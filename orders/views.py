import requests
import uuid
import os
import traceback # Added for detailed error logs
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, CreateOrderSerializer
from cart.models import Cart
from .tasks import send_order_confirmation, send_payment_success_email

class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options', 'delete']
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()] 
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_id = serializer.validated_data['cart_id']

        # 1. Retrieve the Cart
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        # 2. Check if Cart is empty
        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # 3. THE TRANSACTION (All or Nothing)
        with transaction.atomic():
            # A. Create the Order
            order = Order.objects.create(user=request.user)

            # B. Move items from Cart to Order
            order_items = []
            for item in cart_items:
                # Check Stock
                variant = item.product_variant
                if variant.inventory_count < item.quantity:
                    # Rollback everything if out of stock
                    raise Exception(f"Not enough stock for {variant}")

                # Create Order Item (Freezing the price)
                current_price = variant.product.base_price + variant.price_adjustment
                
                order_item = OrderItem(
                    order=order,
                    product_variant=variant,
                    quantity=item.quantity,
                    unit_price=current_price
                )
                order_items.append(order_item)

                # Deduct Inventory
                variant.inventory_count -= item.quantity
                variant.save()

            # Bulk create implies faster database performance
            OrderItem.objects.bulk_create(order_items)

            # C. Delete the Cart
            cart.delete()

        # We trigger the task here, AFTER the transaction block closes.
        send_order_confirmation.delay(order.id)

        # Return the receipt
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # Users can only see their own orders
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            # 1. Get the Order safely
            order = get_object_or_404(Order, id=order_id, user=request.user)
            
            # 2. Check if already paid
            if hasattr(order, 'payment') and order.payment.status == "Completed":
                return Response({"error": "Order already paid"}, status=status.HTTP_400_BAD_REQUEST)

            # 3. Calculate Total Price
            total_price = sum(item.get_total_price() for item in order.items.all())
            
            # Safety Check: Cannot pay for free/empty orders
            if total_price <= 0:
                return Response({"error": "Order total is zero"}, status=status.HTTP_400_BAD_REQUEST)

            # 4. Get API Key Safely
            chapa_key = getattr(settings, 'CHAPA_SECRET_KEY', None)
            if not chapa_key:
                return Response({"error": "CHAPA_SECRET_KEY is missing in settings.py"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 5. Generate unique transaction ref
            tx_ref = str(uuid.uuid4())

            # 6. Chapa Payload
            payload = {
                "amount": str(total_price),
                "currency": "ETB",
                "email": request.user.email,
                "first_name": request.user.first_name or "Guest",
                "last_name": request.user.last_name or "User",
                "tx_ref": tx_ref,
                # --- FIX IS HERE: I removed '/orders' from the URL ---
                "return_url": f"http://127.0.0.1:8000/api/v1/payment/verify/{tx_ref}/"
            }

            headers = {
                "Authorization": f"Bearer {chapa_key}",
                "Content-Type": "application/json"
            }

            # 7. Call Chapa API
            try:
                response = requests.post("https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
                data = response.json()
            except Exception as api_error:
                return Response({"error": "Failed to connect to Chapa", "details": str(api_error)}, status=status.HTTP_502_BAD_GATEWAY)

            if data.get('status') == 'success':
                # 8. Create Payment Record
                Payment.objects.create(
                    order=order,
                    transaction_id=tx_ref,
                    amount=total_price,
                    status="Pending"
                )
                return Response({
                    "payment_url": data['data']['checkout_url'],
                    "tx_ref": tx_ref
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Chapa rejected the request", "details": data}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Print the actual error to your terminal
            print("PAYMENT ERROR:", str(e))
            traceback.print_exc()
            return Response({"error": "An internal error occurred", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    def get(self, request, tx_ref):
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
            
            headers = {
                "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
            }
            
            # 1. Verify with Chapa
            response = requests.get(f"https://api.chapa.co/v1/transaction/verify/{tx_ref}", headers=headers)
            data = response.json()

            if data.get('status') == 'success':
                # 2. Update Payment
                payment.status = "Completed"
                payment.save()

                # 3. Update Order Status
                payment.order.payment_status = 'C' # 'C' = Complete
                payment.order.save()

                # 4. Trigger Celery Task
                send_payment_success_email.delay(payment.order.id)

                return Response({"message": "Payment Successful"}, status=status.HTTP_200_OK)
            else:
                payment.status = "Failed"
                payment.save()
                payment.order.payment_status = 'F'
                payment.order.save()
                return Response({"message": "Payment Failed"}, status=status.HTTP_400_BAD_REQUEST)

        except Payment.DoesNotExist:
            return Response({"error": "Invalid Transaction"}, status=status.HTTP_404_NOT_FOUND)
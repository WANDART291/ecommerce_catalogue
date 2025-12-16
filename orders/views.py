from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from cart.models import Cart
from .tasks import send_order_confirmation  # <--- NEW IMPORT

class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options', 'delete']
    
    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()] # You must be logged in to checkout
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
                # We use the variant's current price, NOT the cart price (for security)
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

        # <--- NEW PART START --->
        # We trigger the task here, AFTER the transaction block closes.
        # This ensures the order is fully saved in the DB before Celery tries to read it.
        send_order_confirmation.delay(order.id)
        # <--- NEW PART END --->

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

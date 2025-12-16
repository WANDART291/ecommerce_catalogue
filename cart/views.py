from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, AddCartItemSerializer, CartItemSerializer
from catalogue.models import ProductVariant

class CartViewSet(mixins.CreateModelMixin, 
                  mixins.RetrieveModelMixin, 
                  mixins.DestroyModelMixin, 
                  viewsets.GenericViewSet):
    """
    Standard ViewSet for creating and retrieving the Cart.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    """
    Handles adding/removing items from a specific cart.
    """
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def create(self, request, *args, **kwargs):
        # Custom logic to handle "Add to Cart"
        cart_id = self.kwargs['cart_pk']
        variant_id = request.data.get('product_variant_id')
        quantity = int(request.data.get('quantity', 1))

        # 1. Get or Create the Item
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_variant_id=variant_id)
            # If item exists, just add to quantity
            cart_item.quantity += quantity
            cart_item.save()
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            # If item does not exist, create it manually
            variant = ProductVariant.objects.get(id=variant_id)
            cart_item = CartItem.objects.create(cart_id=cart_id, product_variant=variant, quantity=quantity)
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

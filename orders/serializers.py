from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product_variant.product.name', read_only=True)
    variant_label = serializers.CharField(source='product_variant.__str__', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'variant_label', 'quantity', 'unit_price', 'get_total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'user', 'items']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        # We verify this ID exists in the views, but checking valid UUID format happens here
        return cart_id

    def save(self, **kwargs):
        # The actual logic moves to the View to keep the Serializer clean
        pass
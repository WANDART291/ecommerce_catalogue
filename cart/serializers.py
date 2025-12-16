from rest_framework import serializers
from .models import Cart, CartItem
from catalogue.serializers import ProductVariantSerializer

class CartItemSerializer(serializers.ModelSerializer):
    # Nesting the variant info so the frontend shows "Air Jordan - Red" automatically
    product_variant = ProductVariantSerializer(read_only=True)
    # We also calculate the subtotal for this specific line item
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'quantity', 'sub_total']

    def get_sub_total(self, obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'grand_total']

    def get_grand_total(self, obj):
        return obj.get_total_price()

# Special Serializer just for ADDING items (keeps the API simple)
class AddCartItemSerializer(serializers.ModelSerializer):
    product_variant_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['product_variant_id', 'quantity']

    def validate_product_variant_id(self, value):
        from catalogue.models import ProductVariant
        if not ProductVariant.objects.filter(id=value).exists():
            raise serializers.ValidationError("This product variant does not exist.")
        return value
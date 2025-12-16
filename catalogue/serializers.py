from rest_framework import serializers
from .models import Product, Brand, Category, ProductVariant, ProductImage, AttributeValue

# -----------------------------
# 1. HELPER SERIALIZERS
# -----------------------------

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'display_order']

class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = AttributeValue
        fields = ['id', 'attribute_name', 'value']

class ProductVariantSerializer(serializers.ModelSerializer):
    attribute_values = AttributeValueSerializer(many=True, read_only=True)
    final_price = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'sku_variant', 'name', 'price_adjustment', 'final_price', 'inventory_count', 'attribute_values']

    def get_final_price(self, obj):
        # Calculate: Base Product Price + Variant Adjustment
        return obj.product.base_price + obj.price_adjustment

    def get_name(self, obj):
        # Generates "Red / Large" automatically
        values = [av.value for av in obj.attribute_values.all()]
        return " / ".join(values)

# -----------------------------
# 2. LIST SERIALIZER (Lightweight for Feeds)
# -----------------------------

class ProductListSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_names = serializers.SerializerMethodField()
    price_range = serializers.SerializerMethodField()
    main_image = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'brand_name', 'category_names', 
            'base_price', 'price_range', 'main_image', 
            'is_available', 'created_at'
        ]

    def get_category_names(self, obj):
        # Returns ["Electronics", "Laptops"] instead of IDs
        return [cat.name for cat in obj.categories.all()]

    def get_price_range(self, obj):
        # Advanced: Checks all variants to show "$100 - $120"
        variants = obj.variants.all()
        if not variants:
            return f"{obj.base_price}"
        
        prices = [obj.base_price + v.price_adjustment for v in variants]
        min_price = min(prices)
        max_price = max(prices)
        
        if min_price == max_price:
            return f"{min_price}"
        return f"{min_price} - {max_price}"

    def get_main_image(self, obj):
        # Grabs the first image efficiently
        image = obj.images.first()
        if image:
            return image.image.url
        return None

    def get_is_available(self, obj):
        # Returns True if ANY variant has stock
        if obj.variants.exists():
            return any(v.inventory_count > 0 for v in obj.variants.all())
        return True # Fallback for simple products

# -----------------------------
# 3. DETAIL SERIALIZER (Heavy for Product Page)
# -----------------------------

class ProductDetailSerializer(ProductListSerializer):
    # Expands everything: Full brand details, all images, full variant list
    brand = BrandSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ['description', 'brand', 'categories', 'images', 'variants']
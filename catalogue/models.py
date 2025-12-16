from django.db import models
from django.conf import settings

# 1. BRAND (e.g., Nike, Apple)
class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True) 
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

# 2. CATEGORY (Recursive: Electronics -> Laptops)
class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

# 3. ATTRIBUTES (e.g., The concept of "Color" or "Size")
class Attribute(models.Model):
    name = models.CharField(max_length=50) # e.g. "Color"

    def __str__(self):
        return self.name

# 4. ATTRIBUTE VALUES (e.g., "Red", "Blue", "Small")
class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=50) # e.g. "Red"

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

# 5. PRODUCT (The main item)
class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    categories = models.ManyToManyField(Category, related_name='products')
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    sku_base = models.CharField(max_length=100, unique=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# 6. PRODUCT VARIANTS (e.g., The specific Red Small Shirt)
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    attribute_values = models.ManyToManyField(AttributeValue, related_name='variants')
    
    sku_variant = models.CharField(max_length=100, unique=True)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    inventory_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} (Variant: {self.sku_variant})"

# 7. IMAGES
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="products/%Y/%m/%d/")
    alt_text = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

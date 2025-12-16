from django.contrib import admin
from .models import Brand, Category, Attribute, AttributeValue, Product, ProductVariant, ProductImage

# 1. Brand Admin
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

# 2. Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)} # Automatically fills slug when typing name
    search_fields = ('name',)

# 3. Attribute Setup (e.g., Color/Size)
class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline] # Allows adding values (Red, Blue) directly inside Attribute

# --- NEW: Register AttributeValue separately so it appears in the sidebar ---
@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('value', 'attribute')
    list_filter = ('attribute',)

# 4. Product Admin
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    show_change_link = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'base_price', 'is_active', 'created_at')
    list_filter = ('is_active', 'brand', 'created_at')
    search_fields = ('name', 'sku_base')
    inlines = [ProductImageInline, ProductVariantInline] # Add images and variants directly on Product page

# 5. Register the rest normally
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
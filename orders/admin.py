from django.contrib import admin
from .models import Order, OrderItem, Payment

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['product_variant', 'quantity', 'unit_price']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'placed_at', 'payment_status']
    list_filter = ['payment_status', 'placed_at']
    inlines = [OrderItemInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # I removed 'timestamp' from here to fix the crash
    list_display = ['transaction_id', 'order', 'amount', 'status']
    list_filter = ['status']

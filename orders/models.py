from django.db import models
from django.conf import settings
from uuid import uuid4
from catalogue.models import ProductVariant

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Complete'),
        ('F', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='orders')
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default='P')
    
    # Simple shipping info for now
    shipping_address = models.TextField(blank=True)
    
    def __str__(self):
        return f"Order {self.id} ({self.payment_status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    
    # We freeze the price here so it doesn't change if the product price changes later
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product_variant} in Order {self.order.id}"

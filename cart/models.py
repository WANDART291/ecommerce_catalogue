from django.db import models
from uuid import uuid4
from django.conf import settings
from catalogue.models import ProductVariant

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: Link to a user if they are logged in
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
   
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = [['cart', 'product_variant']] # Prevent duplicate rows for same item

    def __str__(self):
        return f"{self.quantity} x {self.product_variant}"

    def get_total_price(self):
        # Calculate: Quantity * (Base Price + Adjustment)
        price = self.product_variant.product.base_price + self.product_variant.price_adjustment
        return price * self.quantity

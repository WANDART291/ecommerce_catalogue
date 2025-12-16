from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
# This creates /api/v1/cart/ (To get your cart)
router.register(r'cart', CartViewSet, basename='cart')

# This creates /api/v1/cart/{cart_id}/items/ (To add/remove items)
item_router = DefaultRouter()
item_router.register(r'items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/<uuid:cart_pk>/', include(item_router.urls)),
]
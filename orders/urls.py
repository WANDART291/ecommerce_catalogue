from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    # Existing Order Routes (Create, List, etc.)
    path('', include(router.urls)),

    # New Payment Routes
    path('payment/initiate/<uuid:order_id>/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payment/verify/<str:tx_ref>/', VerifyPaymentView.as_view(), name='verify-payment'),
]
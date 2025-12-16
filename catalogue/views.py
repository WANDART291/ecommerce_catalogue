from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator      # <--- NEW
from django.views.decorators.cache import cache_page      # <--- NEW

from .models import Product, Brand, Category
from .serializers import (
    ProductListSerializer, 
    ProductDetailSerializer, 
    BrandSerializer, 
    CategorySerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    lookup_field = 'id'
    
    # Security
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Tools: Search, Filter, Order
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    filterset_fields = ['brand', 'categories']
    search_fields = ['name', 'description', 'brand__name', 'categories__name']
    ordering_fields = ['base_price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer

    # --- NEW: Cache the List View for 15 minutes ---
    # This tells Django: "Don't run the database query every time. 
    # Just serve the saved result from Redis for the next 900 seconds."
    @method_decorator(cache_page(60 * 15)) 
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
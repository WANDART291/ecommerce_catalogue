from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Product, Brand, Category

class ProductAPITests(APITestCase):
    
    def setUp(self):
        """
        Setup runs BEFORE every single test.
        """
        # Create Brands
        self.nike = Brand.objects.create(name="Nike")
        self.adidas = Brand.objects.create(name="Adidas")
        
        # Create Categories (Explicit slugs to prevent errors)
        self.sneakers = Category.objects.create(name="Sneakers", slug="sneakers")
        self.boots = Category.objects.create(name="Boots", slug="boots")
        
        # Create Product 1: Air Jordan
        self.jordan = Product.objects.create(
            name="Air Jordan 1",
            brand=self.nike,
            base_price=150.00,
            is_active=True,
            sku_base="JORDAN-001"  # <--- FIXED: Added Unique SKU
        )
        self.jordan.categories.add(self.sneakers)

        # Create Product 2: Yeezy
        self.yeezy = Product.objects.create(
            name="Yeezy Boost",
            brand=self.adidas,
            base_price=200.00,
            is_active=True,
            sku_base="YEEZY-001"   # <--- FIXED: Added Unique SKU
        )
        self.yeezy.categories.add(self.boots)

    # --- TEST 1: Can we see the list? ---
    def test_get_product_list(self):
        url = '/api/v1/catalogue/products/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # --- TEST 2: Can we see a specific product? ---
    def test_get_product_detail(self):
        url = f'/api/v1/catalogue/products/{self.jordan.id}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Air Jordan 1")

    # --- TEST 3: Does Search work? ---
    def test_search_product(self):
        url = '/api/v1/catalogue/products/?search=Jordan'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertNotEqual(response.data[0]['name'], "Yeezy Boost")

    # --- TEST 4: Does Filtering work? ---
    def test_filter_by_category(self):
        url = f'/api/v1/catalogue/products/?categories={self.boots.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Yeezy Boost")

    # --- TEST 5: Error Handling ---
    def test_get_invalid_product(self):
        url = '/api/v1/catalogue/products/9999/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

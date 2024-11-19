from django.test import TestCase
from django.urls import reverse
from .models import Product, Category
from accounts.models import User

class ProductTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            sku='TEST123',
            description='Test Description',
            price=99.99,
            stock_quantity=10,
            reorder_level=5
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.stock_quantity, 10)

    def test_product_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inventory:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product') 
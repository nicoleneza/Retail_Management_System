from django.db import models
from django.contrib.auth import get_user_model
from inventory.models import Product
from django.contrib.auth.models import User

User = get_user_model()

class Customer(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    join_date = models.DateTimeField()

class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=10, unique=True)
    district = models.CharField(max_length=50)
class Sale(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile', 'Mobile Payment'),
    )
    
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_sales')
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_sales')
    date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    points_earned = models.IntegerField()
    points_used = models.IntegerField()

    def __str__(self):
        return f"Invoice #{self.invoice_number}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"
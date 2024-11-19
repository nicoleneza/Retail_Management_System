from django.db import models
from django.contrib.auth import get_user_model
from inventory.models import Product

User = get_user_model()

class Sale(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile', 'Mobile Payment'),
    )
    
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               limit_choices_to={'user_type': 'customer'},
                               related_name='purchases')
    staff_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   limit_choices_to={'user_type': 'staff'},
                                   related_name='sales')
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='cash')
    points_earned = models.IntegerField(default=0)
    points_used = models.IntegerField(default=0)

    def __str__(self):
        return f"Invoice #{self.invoice_number}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"
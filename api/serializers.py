from rest_framework import serializers
from inventory.models import Product, Category
from sales.models import Sale, SaleItem
from orders.models import PurchaseOrder, OrderItem, Supplier
from accounts.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type', 'phone_number', 'address')
        read_only_fields = ('id',) 
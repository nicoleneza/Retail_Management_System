from rest_framework import serializers
from sales.models import Sale, Customer, StaffMember

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class StaffMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMember
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
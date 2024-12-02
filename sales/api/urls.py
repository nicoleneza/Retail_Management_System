from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import SaleViewSet, sales_summary, sales_customers, check_db

router = DefaultRouter()
router.register(r'sales', SaleViewSet, basename='sale')

urlpatterns = [
    path('summary/', sales_summary, name='sales-summary'),
    path('customers/', sales_customers, name='sales-customers'),
    path('check-db/', check_db, name='check-db'),
]

urlpatterns += router.urls
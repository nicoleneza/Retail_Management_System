from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, CategoryViewSet, SaleViewSet,
    OrderViewSet, SupplierViewSet, UserViewSet
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
] 
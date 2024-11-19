from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleListView.as_view(), name='index'),
    path('create/', views.create_sale, name='create_sale'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
]
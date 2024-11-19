from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('api/stats/', views.dashboard_stats, name='api_stats'),
]
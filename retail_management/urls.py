from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('sales/', include('sales.urls')),
    path('orders/', include('orders.urls')),
    path('api/', include('sales.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
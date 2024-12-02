from django.urls import path
from accounts.views import landing_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... existing patterns ...
    path('', landing_page, name='landing_page'),
    # ... existing patterns ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
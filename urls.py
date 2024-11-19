from django.urls import path
from accounts.views import landing_page

urlpatterns = [
    # ... existing patterns ...
    path('', landing_page, name='landing_page'),
    # ... existing patterns ...
] 
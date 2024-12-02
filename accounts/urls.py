from django.urls import path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_views, name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('', views.landing_page, name='landing_page'),
    path('signup/', views.signup_views, name='signup'),
] 
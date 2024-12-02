from django.shortcuts import render
from django.views import View
from .forms import RegisterForm,LoginForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from sales.models import Sale
from .models import UserProfile
from django.contrib.auth.models import User
import json
# # Add your views here, for example:
# class LoginView(View):
#     def get(self, request):
#         return render(request, 'accounts/login.html') 

from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileView(View):
    def get(self, request):
        if request.user.user_type == 'staff':
            return redirect('dashboard:index')
        
        recent_purchases = Sale.objects.filter(
            customer= request.user
        ).order_by('-date')[:5]
        context = {
            'user':request.user,
            'recent_purchase':recent_purchases
        }
        return render(request, 'accounts/profile.html',context)

def signup_views(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            try:
                user = form.save(commit=False)  # Don't save to DB yet
                print(f"Attempting to create user: {user.username}")
                # Check if user already exists
                if not User.objects.filter(username=user.username).exists():
                    user.save()
                    print(f"User created successfully: {user.id}")
                    UserProfile.objects.get_or_create(user=user)
                    return redirect('accounts:login')
                else:
                    print(f"Username {user.username} already exists")
                    messages.error(request, 'Username already exists')
            except Exception as e:
                print(f"Error during signup: {str(e)}")
                messages.error(request, 'Error during signup')
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form':form})
def login_views(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
              
            if user is not None:
                # Create profile before login if it doesn't exist
                try:
                    user.userprofile
                except:
                    UserProfile.objects.create(user=user)
                
                login(request, user)
                if user.user_type == 'staff':
                    return redirect('dashboard:index')
                else:
                    return redirect('accounts:profile')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form':form})


def logout_views(request):
    if request.method=='POST':
        logout(request)
        return redirect('accounts:login')
    
    logout(request)
    return redirect('accounts:login')
def landing_page(request):
    return render(request,'accounts/index.html')

def profile_view(request):
    recent_purchase = Sale.objects.filter(
        customer=request.user
    ).order_by('-date')[:5]  # Gets last 5 purchases
    
    purchase_data = {
        'dates': [purchase.date.strftime('%b %d') for purchase in recent_purchase],
        'amounts': [float(purchase.total) for purchase in recent_purchase]
    }
    
    context = {
        'recent_purchase': recent_purchase,
        'purchase_data': json.dumps(purchase_data),
    }
    return render(request, 'accounts/profile.html', context)
from django.shortcuts import render
from django.views import View
from .forms import RegisterForm,LoginForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout

# # Add your views here, for example:
# class LoginView(View):
#     def get(self, request):
#         return render(request, 'accounts/login.html') 

from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileView(APIView):
    def get(self, request):
        return Response({
            'message': 'Hello, World!',
            'user': str(request.user),
            })

def signup_views(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # user = form.save()
            # login(request, user)
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form':form})

def login_views(request):
    if request.method =='POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
              username = form.cleaned_data['username']
              password = form.cleaned_data['password']
              user = authenticate(request,username=username,password=password)
              
              if user is not None:
                  login(request,user)
                  return redirect('dashboard:index')
              else:
                  #invalid login, handle error
                  pass
    else:
        form = LoginForm
    return render(request, 'login.html', {'form':form})


def logout_views(request):
    if request.method=='POST':
        logout(request)
        return redirect('accounts:login')
    
    logout(request)
    return redirect('accounts:login')
def landing_page(request):
    return render(request,'accounts/index.html')
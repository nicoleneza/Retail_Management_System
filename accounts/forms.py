from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required= True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','user_type','phone_number',
                  'address','password1','password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self,commit=True):
        user = super().save(commit=False)
        # user.set_password(self.cleaned_data['password'])
        user.email= self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class LoginForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password= forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

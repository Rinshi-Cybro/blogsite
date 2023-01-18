from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','username','password1','password2']

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Username","class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Enter Password","class":"form-control"}))       
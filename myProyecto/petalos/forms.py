from django import forms 
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import UserCreationForm

class CustomUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['Primer_Nombre','Segundo_Nombre','email','username','password1','password2']

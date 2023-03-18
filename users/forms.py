from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class NewUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username' , 'email', 'first_name', 'last_name', 'password1', 'password2', 'type')
        labels = {
            'type': 'Account Type',
        }
        widgets = {
            'type': forms.Select(),
            'email': forms.EmailInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'username': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }









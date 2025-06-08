from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms


class UserCreationForm(UserCreationForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'username')


class UserChangeForm(UserChangeForm):

    class Meta:
        model =User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 
                  'username', 'is_active', 'is_staff', 'is_superuser',
                  'groups', 'user_permissions')
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class WorkStationReg(forms.Form):
    host = forms.CharField(required=False, widget = forms.TextInput(attrs={'readonly':'readonly'}))
    ip_addres = forms.CharField(required=False, widget = forms.TextInput(attrs={'readonly':'readonly'}))
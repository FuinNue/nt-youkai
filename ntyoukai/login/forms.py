from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ntyoukai.settings import ALPHA_MAXIMUM_USERS

class LoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'password']

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
    	if User.objects.all().count() > ALPHA_MAXIMUM_USERS:
    		raise ValidationError("Maximum users during alpha has been reached.")
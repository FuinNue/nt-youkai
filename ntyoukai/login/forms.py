from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from ntyoukai.settings import ALPHA_MAXIMUM_USERS

class LoginForm(forms.ModelForm):
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

    def validate_alpha_maximum_users(self):
    	if User.objects.all().count > ALPHA_MAXIMUM_USERS:
    		raise ValidationError("Maximum users during alpha has been reached.")
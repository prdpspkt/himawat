from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from .models import User


class UserRegistrationForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """User profile edit form"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar', 'phone']
    
    phone = forms.CharField(max_length=50, required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add phone field if it doesn't exist in model
        if not hasattr(self.instance, 'phone'):
            self.fields.pop('phone', None)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email


class UserLoginForm(forms.Form):
    """User login form"""
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, UpdateView, TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import UserRegistrationForm, UserProfileForm
from .models import User


class RegisterView(CreateView):
    """User registration view"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = '/'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after registration
        user = form.instance
        login(self.request, user)
        messages.success(self.request, 'Registration successful! Welcome to Thelix.')
        return response
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('cms:home')
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        # Update last login timestamp
        user = form.get_user()
        user.last_login_at = timezone.now()
        user.save(update_fields=['last_login_at'])
        
        messages.success(self.request, f'Welcome back, {user.name}!')
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirect admin users to dashboard
        if self.request.user.is_admin:
            return '/dashboard/'
        return super().get_success_url()


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """User profile edit view"""
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

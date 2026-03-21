from django import forms
from django.db import models
from django.contrib.contenttypes.models import ContentType
from .models import Page, Post, FAQ, Product, Category
from .widgets import TinyMCEWidget


class PageForm(forms.ModelForm):
    """Form for Page model"""
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'content': TinyMCEWidget(),
        }


class PostForm(forms.ModelForm):
    """Form for Post model"""
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': TinyMCEWidget(),
        }


class FAQForm(forms.ModelForm):
    """Form for FAQ model"""
    class Meta:
        model = FAQ
        fields = '__all__'
        widgets = {
            'answer': TinyMCEWidget(),
        }


class ProductForm(forms.ModelForm):
    """Form for Product model"""
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': TinyMCEWidget(),
        }


class CategoryForm(forms.ModelForm):
    """Form for Category model with filtered applies_to field"""
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter applies_to to show only specific content types without duplicates
        # We want: post (cms), page (cms), service (services), training (dashboard)
        self.fields['applies_to'].queryset = ContentType.objects.filter(
            models.Q(app_label='cms', model='post') |
            models.Q(app_label='cms', model='page') |
            models.Q(app_label='services', model='service') |
            models.Q(app_label='dashboard', model='training')
        ).order_by('model')

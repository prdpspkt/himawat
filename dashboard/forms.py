from django import forms
from .models import Page, Post, FAQ, Product
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

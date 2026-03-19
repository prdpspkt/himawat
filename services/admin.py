from django.contrib import admin
from .models import ServiceCategory, Service


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'sort_order', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['sort_order', 'status']
    ordering = ['sort_order', 'name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'slug', 'price', 'is_featured', 'status', 'sort_order', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'short_description', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['sort_order', 'status', 'is_featured']
    ordering = ['sort_order', 'title']
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'title', 'slug', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('icon', 'image', 'featured_image')
        }),
        ('Pricing', {
            'fields': ('price', 'price_display'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('sort_order', 'is_featured', 'status')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )

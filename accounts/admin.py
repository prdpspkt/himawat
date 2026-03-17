from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'name', 'role', 'status', 'avatar_preview', 'last_login_at', 'created_at']
    list_filter = ['role', 'status', 'is_staff', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_editable = ['role', 'status']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {
            'fields': ('avatar', 'role', 'status', 'email_verified', 'email_verified_at', 'last_login_at')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'status'),
        }),
    )
    
    readonly_fields = ['email_verified_at', 'last_login_at', 'created_at', 'updated_at']
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%;" />', obj.avatar.url)
        return format_html('<div style="width: 40px; height: 40px; border-radius: 50%; background: #ccc; display: flex; align-items: center; justify-content: center; color: #666;">{}</div>', obj.username[0].upper() if obj.username else '?')
    avatar_preview.short_description = 'Avatar'
    
    def name(self, obj):
        return obj.name
    name.short_description = 'Full Name'

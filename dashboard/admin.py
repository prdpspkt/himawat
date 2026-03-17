from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from dashboard.models import (
    Category, Tag, Post, Page, Download, Gallery, GalleryImage,
    Testimonial, Carousel, FAQ, Product, ProductImage,
    ProductRequest, ProductRequestItem, Consultation, ConsultationFile,
    Menu, MenuItem, CompanyInfo, CEOInfo, PageRevision, PostRevision, AIConfiguration
)
from dashboard.forms import PageForm, PostForm, FAQForm, ProductForm


# Custom admin site configuration
admin.site.site_header = 'Thelix Administration'
admin.site.site_title = 'Thelix Admin'
admin.site.index_title = 'Dashboard'


class BaseAdmin(admin.ModelAdmin):
    """Base admin with common functionality"""
    list_per_page = 25
    
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['created_at', 'updated_at']
        return []


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'parent', 'post_count', 'status', 'sort_order']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['status', 'sort_order']
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Posts'


@admin.register(Tag)
class TagAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['status']


@admin.register(Post)
class PostAdmin(BaseAdmin):
    form = PostForm
    list_display = ['title', 'author', 'category', 'status', 'view_count', 'published_at', 'featured_image_preview']
    list_filter = ['status', 'category', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt', 'keywords']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    date_hierarchy = 'published_at'
    filter_horizontal = ['tags']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('Organization', {
            'fields': ('category', 'tags', 'author')
        }),
        ('Settings', {
            'fields': ('status', 'allow_comments', 'published_at')
        }),
        ('SEO', {
            'fields': ('keywords', 'custom_fields'),
            'classes': ('collapse',)
        }),
    )

    def featured_image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.featured_image.url)
        return '-'
    featured_image_preview.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Page)
class PageAdmin(BaseAdmin):
    form = PageForm
    list_display = ['title', 'slug', 'parent', 'template', 'status', 'order', 'updated_at']
    list_filter = ['status', 'template', 'created_at']
    search_fields = ['title', 'content', 'meta_title', 'meta_description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'order', 'template']

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('Hierarchy', {
            'fields': ('parent', 'order')
        }),
        ('Template & Settings', {
            'fields': ('template', 'status')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Page Builder', {
            'fields': ('blocks',),
            'classes': ('collapse',)
        }),
    )


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ['image', 'title', 'alt_text', 'sort_order']


@admin.register(Gallery)
class GalleryAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'image_count', 'status', 'sort_order', 'cover_preview']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['status', 'sort_order']
    inlines = [GalleryImageInline]
    
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.cover_image.url)
        return '-'
    cover_preview.short_description = 'Cover'
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'


@admin.register(Download)
class DownloadAdmin(BaseAdmin):
    list_display = ['title', 'file_type', 'download_count', 'file_size_display', 'status', 'published_at']
    list_filter = ['status', 'file_type', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    
    def file_size_display(self, obj):
        if obj.file_size < 1024:
            return f"{obj.file_size} B"
        elif obj.file_size < 1024 * 1024:
            return f"{obj.file_size / 1024:.1f} KB"
        else:
            return f"{obj.file_size / (1024 * 1024):.1f} MB"
    file_size_display.short_description = 'Size'


@admin.register(Testimonial)
class TestimonialAdmin(BaseAdmin):
    list_display = ['name', 'company', 'position', 'rating', 'featured', 'status', 'avatar_preview']
    list_filter = ['status', 'featured', 'rating', 'created_at']
    search_fields = ['name', 'testimonial', 'company']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['status', 'featured', 'rating']
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width: 40px; height: 40px; border-radius: 50%;" />', obj.avatar.url)
        return format_html('<div style="width: 40px; height: 40px; border-radius: 50%; background: #ccc; display: flex; align-items: center; justify-content: center;">{}</div>', obj.name[0] if obj.name else '?')
    avatar_preview.short_description = 'Avatar'


@admin.register(Carousel)
class CarouselAdmin(BaseAdmin):
    list_display = ['title', 'sort_order', 'status', 'image_preview', 'link_url']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'caption']
    list_editable = ['sort_order', 'status']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


@admin.register(FAQ)
class FAQAdmin(BaseAdmin):
    form = FAQForm
    list_display = ['question_preview', 'category', 'sort_order', 'status']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['sort_order', 'status']

    def question_preview(self, obj):
        return obj.question[:80] + '...' if len(obj.question) > 80 else obj.question
    question_preview.short_description = 'Question'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'sort_order', 'is_primary']


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    form = ProductForm
    list_display = ['name', 'category', 'featured', 'status', 'sort_order', 'image_preview']
    list_filter = ['category', 'status', 'featured', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['category', 'featured', 'status', 'sort_order']
    inlines = [ProductImageInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Image'


class ProductRequestItemInline(admin.TabularInline):
    model = ProductRequestItem
    extra = 0
    autocomplete_fields = ['product']


@admin.register(ProductRequest)
class ProductRequestAdmin(BaseAdmin):
    list_display = ['id', 'name', 'email', 'status', 'total_items', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at', 'total_items', 'total_quantity']
    inlines = [ProductRequestItemInline]
    
    fieldsets = (
        ('Request Info', {
            'fields': ('name', 'email', 'phone', 'message', 'created_at', 'total_items', 'total_quantity')
        }),
        ('Admin', {
            'fields': ('status', 'notes')
        }),
    )


@admin.register(ProductRequestItem)
class ProductRequestItemAdmin(BaseAdmin):
    list_display = ['request', 'product', 'quantity', 'created_at']
    list_filter = ['created_at']
    autocomplete_fields = ['request', 'product']


class ConsultationFileInline(admin.TabularInline):
    model = ConsultationFile
    extra = 0
    readonly_fields = ['filename', 'file_type', 'file_size', 'created_at']


@admin.register(Consultation)
class ConsultationAdmin(BaseAdmin):
    list_display = ['id', 'subject', 'name', 'email', 'preferred_date', 'status', 'created_at']
    list_filter = ['status', 'preferred_date', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at']
    inlines = [ConsultationFileInline]
    
    fieldsets = (
        ('Request Info', {
            'fields': ('name', 'email', 'phone', 'subject', 'message', 'preferred_date', 'created_at')
        }),
        ('Admin', {
            'fields': ('status', 'notes')
        }),
    )


@admin.register(ConsultationFile)
class ConsultationFileAdmin(BaseAdmin):
    list_display = ['filename', 'consultation', 'file_type', 'file_size_formatted', 'created_at']
    list_filter = ['file_type', 'created_at']
    
    def file_size_formatted(self, obj):
        if obj.file_size < 1024:
            return f"{obj.file_size} B"
        elif obj.file_size < 1024 * 1024:
            return f"{obj.file_size / 1024:.1f} KB"
        else:
            return f"{obj.file_size / (1024 * 1024):.1f} MB"
    file_size_formatted.short_description = 'Size'


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ['title', 'type', 'page', 'url', 'order', 'parent', 'is_active']
    autocomplete_fields = ['page', 'parent']


@admin.register(MenuItem)
class MenuItemAdmin(BaseAdmin):
    list_display = ['title', 'menu', 'type', 'order', 'is_active']
    list_filter = ['menu', 'type', 'is_active']
    search_fields = ['title', 'url']
    list_editable = ['order', 'is_active']


@admin.register(Menu)
class MenuAdmin(BaseAdmin):
    list_display = ['name', 'slug', 'location', 'item_count']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [MenuItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'


@admin.register(CEOInfo)
class CEOInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'is_active', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'message', 'photo', 'is_active')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Social Media', {
            'fields': ('social_linkedin', 'social_twitter', 'social_facebook')
        }),
    )


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Company Details', {
            'fields': ('company_name', 'description', 'logo', 'favicon')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address', 'city', 'state', 'postal_code', 'country')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude'),
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'whatsapp')
        }),
    )

    def has_add_permission(self, request):
        # Only allow one instance
        return not CompanyInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PageRevision)
class PageRevisionAdmin(BaseAdmin):
    list_display = ['page', 'revision_number', 'created_by', 'created_at', 'is_auto_save']
    list_filter = ['is_auto_save', 'created_at']
    search_fields = ['page__title', 'title', 'revision_reason']
    readonly_fields = ['page', 'revision_number', 'title', 'content', 'excerpt', 'meta_title',
                      'meta_description', 'meta_keywords', 'template', 'blocks', 'created_at', 'created_by']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PostRevision)
class PostRevisionAdmin(BaseAdmin):
    list_display = ['post', 'revision_number', 'created_by', 'created_at', 'is_auto_save']
    list_filter = ['is_auto_save', 'created_at']
    search_fields = ['post__title', 'title', 'revision_reason']
    readonly_fields = ['post', 'revision_number', 'title', 'content', 'excerpt', 'status',
                      'published_at', 'revision_reason', 'created_at', 'created_by', 'is_auto_save']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(AIConfiguration)
class AIConfigurationAdmin(BaseAdmin):
    list_display = ['name', 'model', 'status', 'is_default', 'created_at']
    list_filter = ['status', 'model', 'created_at']
    search_fields = ['name', 'model']
    list_editable = ['status', 'is_default']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model', 'status', 'is_default')
        }),
        ('API Configuration', {
            'fields': ('api_key',)
        }),
        ('AI Settings', {
            'fields': ('system_prompt', 'max_tokens', 'temperature'),
            'description': 'Configure how the AI should behave. System prompt defines the AI persona and behavior.'
        }),
    )

    def save_model(self, request, obj, form, change):
        # Ensure only one configuration is marked as default
        if obj.is_default:
            AIConfiguration.objects.filter(is_default=True).update(is_default=False)
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

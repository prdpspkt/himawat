from django.urls import path
from . import views
from . import menu_views
from . import media_views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    
    # Content Management
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    path('pages/', views.PageListView.as_view(), name='page_list'),
    path('pages/create/', views.PageCreateView.as_view(), name='page_create'),
    path('pages/<int:pk>/edit/', views.PageUpdateView.as_view(), name='page_edit'),
    path('pages/<int:pk>/delete/', views.PageDeleteView.as_view(), name='page_delete'),
    
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    path('downloads/', views.DownloadListView.as_view(), name='download_list'),
    path('downloads/create/', views.DownloadCreateView.as_view(), name='download_create'),
    path('downloads/<int:pk>/edit/', views.DownloadUpdateView.as_view(), name='download_edit'),
    path('downloads/<int:pk>/delete/', views.DownloadDeleteView.as_view(), name='download_delete'),
    
    path('galleries/', views.GalleryListView.as_view(), name='gallery_list'),
    path('galleries/create/', views.GalleryCreateView.as_view(), name='gallery_create'),
    path('galleries/<int:pk>/edit/', views.GalleryUpdateView.as_view(), name='gallery_edit'),
    path('galleries/<int:pk>/delete/', views.GalleryDeleteView.as_view(), name='gallery_delete'),
    
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('videos/create/', views.VideoCreateView.as_view(), name='video_create'),
    path('videos/<int:pk>/edit/', views.VideoUpdateView.as_view(), name='video_edit'),
    path('videos/<int:pk>/delete/', views.VideoDeleteView.as_view(), name='video_delete'),
    
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('testimonials/create/', views.TestimonialCreateView.as_view(), name='testimonial_create'),
    path('testimonials/<int:pk>/edit/', views.TestimonialUpdateView.as_view(), name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', views.TestimonialDeleteView.as_view(), name='testimonial_delete'),
    
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    
    path('carousels/', views.CarouselListView.as_view(), name='carousel_list'),
    path('carousels/create/', views.CarouselCreateView.as_view(), name='carousel_create'),
    path('carousels/<int:pk>/edit/', views.CarouselUpdateView.as_view(), name='carousel_edit'),
    path('carousels/<int:pk>/delete/', views.CarouselDeleteView.as_view(), name='carousel_delete'),
    
    path('faqs/', views.FAQListView.as_view(), name='faq_list'),
    path('faqs/create/', views.FAQCreateView.as_view(), name='faq_create'),
    path('faqs/<int:pk>/edit/', views.FAQUpdateView.as_view(), name='faq_edit'),
    path('faqs/<int:pk>/delete/', views.FAQDeleteView.as_view(), name='faq_delete'),
    
    # Menu Management - Dynamic menu system
    path('menus/', views.MenuListView.as_view(), name='menu_list'),
    path('menus/create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('menus/<int:pk>/edit/', views.MenuUpdateView.as_view(), name='menu_edit'),
    path('menus/<int:pk>/items/', menu_views.menu_items_manage, name='menu_items'),
    path('menus/<int:pk>/delete/', views.MenuDeleteView.as_view(), name='menu_delete'),
    
    # Menu Management API
    path('api/menu-items/create/', menu_views.menu_item_create_ajax, name='menu_item_create_ajax'),
    path('api/menu-items/<int:pk>/update/', menu_views.menu_item_update_ajax, name='menu_item_update_ajax'),
    path('api/menu-items/<int:pk>/delete/', menu_views.menu_item_delete_ajax, name='menu_item_delete_ajax'),
    path('api/menu-items/<int:pk>/get/', menu_views.menu_item_get_ajax, name='menu_item_get_ajax'),
    path('api/menu-items/reorder/', menu_views.menu_item_reorder_ajax, name='menu_item_reorder_ajax'),
    
    # Gallery Image API
    path('api/gallery/images/upload/', views.gallery_image_upload, name='gallery_image_upload'),
    path('api/gallery/images/reorder/', views.gallery_image_reorder, name='gallery_image_reorder'),
    path('api/gallery/images/<int:pk>/delete/', views.gallery_image_delete, name='gallery_image_delete'),
    path('api/gallery/images/<int:pk>/', views.gallery_image_detail, name='gallery_image_detail'),
    path('api/gallery/images/<int:pk>/update/', views.gallery_image_update, name='gallery_image_update'),
    
    # Category and Tag AJAX API
    path('api/categories/create/', views.category_create_ajax, name='category_create_ajax'),
    path('api/tags/create/', views.tag_create_ajax, name='tag_create_ajax'),

    # Requests & Consultations
    path('product-requests/', views.ProductRequestListView.as_view(), name='product_request_list'),
    path('product-requests/<int:pk>/', views.ProductRequestDetailView.as_view(), name='product_request_detail'),

    path('consultations/', views.ConsultationListView.as_view(), name='consultation_list'),
    path('consultations/<int:pk>/', views.ConsultationDetailView.as_view(), name='consultation_detail'),

    # Profile
    path('profile/', views.UserProfileUpdateView.as_view(), name='user_profile'),

    # User Profile
    path('profile/', views.UserProfileUpdateView.as_view(), name='user_profile'),

    # Settings
    path('settings/company/', views.CompanyInfoUpdateView.as_view(), name='company_info'),
    path('settings/ceo/', views.CEOInfoUpdateView.as_view(), name='ceo_info'),
    path('settings/users/', views.UserListView.as_view(), name='user_list'),

    # Revision Management
    path('pages/<int:page_id>/revisions/', views.PageRevisionListView.as_view(), name='page_revisions'),
    path('posts/<int:post_id>/revisions/', views.PostRevisionListView.as_view(), name='post_revisions'),
    path('revisions/page/<int:revision_id>/restore/', views.restore_page_revision, name='restore_page_revision'),
    path('revisions/post/<int:revision_id>/restore/', views.restore_post_revision, name='restore_post_revision'),

    # AI Configuration Management
    path('settings/ai-config/', views.AIConfigurationListView.as_view(), name='ai_config_list'),
    path('settings/ai-config/create/', views.AIConfigurationCreateView.as_view(), name='ai_config_create'),
    path('settings/ai-config/<int:pk>/edit/', views.AIConfigurationUpdateView.as_view(), name='ai_config_edit'),
    path('settings/ai-config/<int:pk>/delete/', views.AIConfigurationDeleteView.as_view(), name='ai_config_delete'),

    # AI Content Generation API
    path('api/ai/generate/', views.generate_content_with_ai, name='ai_generate_content'),

    # Media Upload API
    path('api/media/upload/', media_views.media_upload, name='media_upload'),
]

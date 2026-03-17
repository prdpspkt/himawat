from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Blog/Posts
    path('blog/', views.PostListView.as_view(), name='post_list'),
    path('blog/category/<slug:category_slug>/', views.PostListView.as_view(), name='post_category'),
    path('blog/tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_tag'),
    path('blog/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Pages
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    
    # Downloads
    path('downloads/', views.DownloadListView.as_view(), name='download_list'),
    path('downloads/<slug:slug>/', views.DownloadDetailView.as_view(), name='download_detail'),
    path('downloads/<slug:slug>/file/', views.download_file, name='download_file'),
    
    # Galleries
    path('galleries/', views.GalleryListView.as_view(), name='gallery_list'),
    path('galleries/<slug:slug>/', views.GalleryDetailView.as_view(), name='gallery_detail'),
    
    # Videos
    path('videos/', views.VideoListView.as_view(), name='video_list'),
    path('videos/<slug:slug>/', views.VideoDetailView.as_view(), name='video_detail'),
    
    # Testimonials
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonial_list'),
    
    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:slug>/request/', views.product_request, name='product_request'),
    
    # Consultation
    path('consultation/', views.ConsultationView.as_view(), name='consultation'),
    path('consultation/submit/', views.consultation_request, name='consultation_submit'),
    
    # Search
    path('search/', views.search, name='search'),
]

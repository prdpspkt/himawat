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

    # Categories
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),

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

    # FAQs
    path('faqs/', views.FAQListView.as_view(), name='faq_list'),

    # Products
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:slug>/request/', views.product_request, name='product_request'),

    # Services
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<slug:slug>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/<slug:slug>/request/', views.service_request, name='service_request'),

    # Trainings
    path('trainings/', views.TrainingListView.as_view(), name='training_list'),
    path('trainings/<slug:slug>/', views.TrainingDetailView.as_view(), name='training_detail'),
    path('trainings/<slug:slug>/request/', views.training_request, name='training_request'),

    # Consultation
    path('consultation/', views.ConsultationView.as_view(), name='consultation'),
    path('consultation/submit/', views.consultation_request, name='consultation_submit'),

    # CEO Profile
    path('ceo/', views.CEOProfileView.as_view(), name='ceo_profile'),

    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),

    # Tools
    path('tools/', views.tools_list, name='tools'),
    path('tools/measurement-converter/', views.measurement_converter, name='measurement_converter'),
    path('tools/area-converter/', views.area_converter, name='area_converter'),

    # Search
    path('search/', views.search, name='search'),
]

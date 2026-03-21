from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from dashboard.models import (
    Post, Page, Category, Tag, Download, Gallery,
    Testimonial, Carousel, FAQ, Product, ProductRequest, Consultation, Video,
    Service, ServiceRequest, Training, TrainingRequest
)


class HomeView(TemplateView):
    """Homepage view"""
    template_name = 'cms/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Carousel slides
        context['carousel_slides'] = Carousel.objects.filter(
            status='active'
        ).order_by('sort_order')
        
        # Featured testimonials
        context['featured_testimonials'] = Testimonial.objects.filter(
            status='published', 
            featured=True
        ).order_by('order')[:3]
        
        # FAQs grouped by category
        context['vastu_faqs'] = FAQ.objects.filter(
            category='vastu', 
            status='active'
        ).order_by('sort_order')
        
        context['engineering_faqs'] = FAQ.objects.filter(
            category='engineering', 
            status='active'
        ).order_by('sort_order')
        
        return context


class PostListView(ListView):
    """Blog post list view"""
    model = Post
    template_name = 'cms/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).select_related('category', 'author').prefetch_related('tags')
        
        # Filter by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tag
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )
        
        return queryset.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(status='active')
        context['tags'] = Tag.objects.filter(status='active')
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['current_tag'] = get_object_or_404(Tag, slug=tag_slug)
        
        return context


class PostDetailView(DetailView):
    """Blog post detail view"""
    model = Post
    template_name = 'cms/post_detail.html'  # Fallback template
    context_object_name = 'post'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        """
        Get template with priority:
        1. Custom template_name field
        2. Slug-based template
        3. Default template
        """
        obj = self.get_object()
        return [obj.get_template()]

    def get_queryset(self):
        return Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).select_related('category', 'author').prefetch_related('tags')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view count
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj

    def get_context_data(self, **kwargs):
        from django.db.models import Count
        from dashboard.models import Category

        context = super().get_context_data(**kwargs)
        post = self.object

        # Related posts
        context['related_posts'] = Post.objects.filter(
            status='published',
            category=post.category
        ).exclude(id=post.id).select_related('category')[:3]

        # Categories with post count
        context['categories'] = Category.objects.filter(
            status='active'
        ).annotate(post_count=Count('posts')).filter(post_count__gt=0)

        # Popular posts (by view count)
        context['popular_posts'] = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).exclude(id=post.id).order_by('-view_count')[:5]

        # Recent posts
        context['recent_posts'] = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).exclude(id=post.id).order_by('-published_at')[:5]

        # Archive (posts grouped by month/year)
        from django.db.models.functions import TruncMonth
        posts_by_month = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).annotate(month=TruncMonth('published_at')).values('month').annotate(
            count=Count('id')
        ).order_by('-month')

        context['archive_months'] = posts_by_month

        return context


class CategoryDetailView(DetailView):
    """Category detail view with dynamic template support"""
    model = Category
    template_name = 'cms/categories/category.html'  # Fallback template
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        """
        Get template with priority:
        1. Custom template_name field
        2. Slug-based template
        3. Default template
        """
        obj = self.get_object()
        return [obj.get_template()]

    def get_queryset(self):
        return Category.objects.filter(status='active').prefetch_related('posts__author', 'pages', 'services', 'trainings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object

        # Get posts in this category
        context['posts'] = Post.objects.filter(
            category=category,
            status='published',
            published_at__lte=timezone.now()
        ).select_related('author').order_by('-published_at')

        # Get pages in this category
        context['pages'] = Page.objects.filter(
            category=category,
            status='active'
        ).order_by('order', 'title')

        # Get services in this category
        context['services'] = Service.objects.filter(
            category=category,
            status='active'
        ).order_by('-featured', 'sort_order', 'name')

        # Get trainings in this category
        context['trainings'] = Training.objects.filter(
            category=category,
            status='active'
        ).order_by('-featured', 'sort_order', 'name')

        # Get child categories if any
        context['child_categories'] = Category.objects.filter(
            parent=category,
            status='active'
        ).order_by('sort_order', 'name')

        return context


class PageDetailView(DetailView):
    """CMS Page detail view with dynamic template support"""
    model = Page
    template_name = 'cms/pages/default.html'  # Fallback template
    context_object_name = 'page'
    slug_url_kwarg = 'slug'

    def get_template_names(self):
        """
        Get template with priority:
        1. Custom template_name field
        2. Preset template field
        3. Slug-based template
        4. Default template
        """
        obj = self.get_object()
        return [obj.get_template()]

    def get_queryset(self):
        return Page.objects.filter(status='active')


def page_detail(request, slug):
    """Page detail view with template priority system"""
    page = get_object_or_404(Page, slug=slug, status='active')

    # Use the get_template method with priority system
    template_name = page.get_template()
    return render(request, template_name, {'page': page})


class DownloadListView(ListView):
    """Downloads list view"""
    model = Download
    template_name = 'cms/download_list.html'
    context_object_name = 'downloads'
    paginate_by = 12
    
    def get_queryset(self):
        return Download.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).order_by('-published_at')


class DownloadDetailView(DetailView):
    """Download detail view"""
    model = Download
    template_name = 'cms/download_detail.html'
    context_object_name = 'download'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Download.objects.filter(status='published')


def download_file(request, slug):
    """Track and serve download file"""
    download = get_object_or_404(Download, slug=slug, status='published')
    download.download_count += 1
    download.save(update_fields=['download_count'])
    
    response = HttpResponse(download.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{download.file.name.split("/")[-1]}"'
    return response


class GalleryListView(ListView):
    """Photo galleries list view"""
    model = Gallery
    template_name = 'cms/gallery_list.html'
    context_object_name = 'galleries'
    paginate_by = 12
    
    def get_queryset(self):
        return Gallery.objects.filter(
            status='active'
        ).annotate(image_count=Count('images')).order_by('sort_order')


class GalleryDetailView(DetailView):
    """Photo gallery detail view"""
    model = Gallery
    template_name = 'cms/gallery_detail.html'
    context_object_name = 'gallery'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Gallery.objects.filter(status='active').prefetch_related('images')


class TestimonialListView(ListView):
    """Testimonials list view"""
    model = Testimonial
    template_name = 'cms/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 12

    def get_queryset(self):
        return Testimonial.objects.filter(
            status='published'
        ).order_by('-featured', 'order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculate average rating
        testimonials = self.get_queryset()
        if testimonials.exists():
            avg_rating = sum(t.rating for t in testimonials) / len(testimonials)
            context['average_rating'] = round(avg_rating, 1)
            context['total_count'] = len(testimonials)
        return context


class FAQListView(TemplateView):
    """FAQ list view"""
    template_name = 'cms/faq_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all active FAQs grouped by category
        vastu_faqs = FAQ.objects.filter(
            category='vastu',
            status='active'
        ).order_by('sort_order')

        engineering_faqs = FAQ.objects.filter(
            category='engineering',
            status='active'
        ).order_by('sort_order')

        context['vastu_faqs'] = vastu_faqs
        context['engineering_faqs'] = engineering_faqs
        context['total_vastu'] = vastu_faqs.count()
        context['total_engineering'] = engineering_faqs.count()

        return context


class ProductListView(ListView):
    """Products list view"""
    model = Product
    template_name = 'cms/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(status='active').select_related('category')

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset.order_by('-featured', 'sort_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get only categories that have active products
        from dashboard.models import Category
        active_categories = Category.objects.filter(
            products__status='active',
            status='active'
        ).distinct().order_by('sort_order', 'name')
        context['categories'] = active_categories
        return context


class ProductDetailView(DetailView):
    """Product detail view"""
    model = Product
    template_name = 'cms/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(status='active').prefetch_related('images')


@require_POST
def product_request(request, slug):
    """Handle product request form"""
    product = get_object_or_404(Product, slug=slug, status='active')
    
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone', '')
    message = request.POST.get('message')
    
    if name and email and message:
        ProductRequest.objects.create(
            product=product,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, 'Your request has been submitted. We will contact you soon!')
    else:
        messages.error(request, 'Please fill in all required fields.')
    
    return redirect('cms:product_detail', slug=slug)


@require_POST
def consultation_request(request):
    """Handle consultation form"""
    from dashboard.models import ConsultationFile

    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone', '')
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    preferred_date = request.POST.get('preferred_date')

    if name and email and subject and message:
        consultation = Consultation.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            preferred_date=preferred_date or None
        )

        # Handle file uploads
        files = request.FILES.getlist('files')
        if files:
            for uploaded_file in files:
                ConsultationFile.objects.create(
                    consultation=consultation,
                    file=uploaded_file
                )

        messages.success(request, 'Your consultation request has been submitted. We will contact you soon!')
    else:
        messages.error(request, 'Please fill in all required fields.')

    return redirect('cms:home')


class ConsultationView(TemplateView):
    """Consultation page view"""
    template_name = 'cms/consultation.html'


# ===== SERVICE VIEWS =====

class ServiceListView(ListView):
    """Service list view"""
    model = Service
    template_name = 'cms/service_list.html'
    context_object_name = 'services'
    paginate_by = 12

    def get_queryset(self):
        queryset = Service.objects.filter(status='active').select_related('category')

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset.order_by('-featured', 'sort_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get only categories that have active services
        from dashboard.models import Category
        active_categories = Category.objects.filter(
            services__status='active',
            status='active'
        ).distinct().order_by('sort_order', 'name')
        context['categories'] = active_categories
        return context


class ServiceDetailView(DetailView):
    """Service detail view"""
    model = Service
    template_name = 'cms/service_detail.html'
    context_object_name = 'service'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Service.objects.filter(status='active')


@require_POST
def service_request(request, slug):
    """Handle service request form"""
    service = get_object_or_404(Service, slug=slug, status='active')

    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone', '')
    message = request.POST.get('message')

    if name and email and message:
        ServiceRequest.objects.create(
            service=service,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, 'Your request has been submitted. We will contact you soon!')
    else:
        messages.error(request, 'Please fill in all required fields.')

    return redirect('pages:service_detail', slug=slug)


class VideoListView(ListView):
    """Video list view"""
    model = Video
    template_name = 'cms/video_list.html'
    context_object_name = 'videos'
    paginate_by = 12
    
    def get_queryset(self):
        return Video.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).order_by('sort_order', '-published_at')


class VideoDetailView(DetailView):
    """Video detail view"""
    model = Video
    template_name = 'cms/video_detail.html'
    context_object_name = 'video'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Video.objects.filter(status='published')


# ===== TRAINING VIEWS =====

class TrainingListView(ListView):
    """Training list view"""
    model = Training
    template_name = 'cms/training_list.html'
    context_object_name = 'trainings'
    paginate_by = 12

    def get_queryset(self):
        queryset = Training.objects.filter(status='active').select_related('category')

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset.order_by('-featured', 'sort_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get only categories that have active trainings
        from dashboard.models import Category
        active_categories = Category.objects.filter(
            trainings__status='active',
            status='active'
        ).distinct().order_by('sort_order', 'name')
        context['categories'] = active_categories
        return context


class TrainingDetailView(DetailView):
    """Training detail view"""
    model = Training
    template_name = 'cms/training_detail.html'
    context_object_name = 'training'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Training.objects.filter(status='active')


@require_POST
def training_request(request, slug):
    """Handle training request form"""
    training = get_object_or_404(Training, slug=slug, status='active')

    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone', '')
    message = request.POST.get('message')

    if name and email and message:
        TrainingRequest.objects.create(
            training=training,
            name=name,
            email=email,
            phone=phone,
            message=message
        )
        messages.success(request, 'Your request has been submitted. We will contact you soon!')
    else:
        messages.error(request, 'Please fill in all required fields.')

    return redirect('pages:training_detail', slug=slug)


def search(request):
    """Global search view"""
    query = request.GET.get('q', '')
    
    if query:
        posts = Post.objects.filter(
            status='published',
            published_at__lte=timezone.now()
        ).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )[:10]
        
        pages = Page.objects.filter(
            status='active'
        ).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )[:10]
        
        products = Product.objects.filter(
            status='active'
        ).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )[:10]
    else:
        posts = []
        pages = []
        products = []
    
    return render(request, 'cms/search.html', {
        'query': query,
        'posts': posts,
        'pages': pages,
        'products': products,
        'total_results': len(posts) + len(pages) + len(products)
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    View, TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse

from dashboard.models import (
    Post, Page, Category, Tag, Download, Gallery,
    Testimonial, Carousel, FAQ, Product, ProductRequest, ProductRequestItem, ProductImage,
    Consultation,
    Menu, CompanyInfo, CEOInfo, Video, PageRevision, PostRevision, AIConfiguration, EmailConfiguration,
    Service, ServiceRequest, Training, TrainingRequest
)
from dashboard.forms import PageForm, PostForm, FAQForm, ProductForm, CategoryForm
from dashboard.decorators import staff_member_required
from accounts.models import User


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Mixin to check if user is admin"""
    def test_func(self):
        return self.request.user.is_admin


class DashboardView(AdminRequiredMixin, TemplateView):
    """Main dashboard view"""
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        context['total_posts'] = Post.objects.count()
        context['published_posts'] = Post.objects.filter(status='published').count()
        context['total_pages'] = Page.objects.count()
        context['total_products'] = Product.objects.count()
        context['total_galleries'] = Gallery.objects.count()
        
        # Recent items
        context['recent_posts'] = Post.objects.select_related('author').order_by('-created_at')[:5]
        context['pending_consultations'] = Consultation.objects.filter(status='pending').count()
        context['pending_product_requests'] = ProductRequest.objects.filter(status='pending').count()
        
        # Popular content
        context['popular_posts'] = Post.objects.order_by('-view_count')[:5]
        
        return context


# Base CRUD Views
class BaseListView(AdminRequiredMixin, ListView):
    """Base list view for dashboard"""
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(name__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class BaseCreateView(AdminRequiredMixin, CreateView):
    """Base create view"""
    def form_valid(self, form):
        messages.success(self.request, f'{self.model.__name__} created successfully!')
        return super().form_valid(form)


class BaseUpdateView(AdminRequiredMixin, UpdateView):
    """Base update view"""
    def form_valid(self, form):
        messages.success(self.request, f'{self.model.__name__} updated successfully!')
        return super().form_valid(form)


class BaseDeleteView(AdminRequiredMixin, DeleteView):
    """Base delete view"""
    def delete(self, request, *args, **kwargs):
        messages.success(request, f'{self.model.__name__} deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Post Views
class PostListView(BaseListView):
    model = Post
    template_name = 'dashboard/post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.select_related('category', 'author').order_by('-created_at')


class PostCreateView(BaseCreateView):
    model = Post
    form_class = PostForm
    template_name = 'dashboard/post_form.html'
    success_url = reverse_lazy('dashboard:post_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.filter(status='active').prefetch_related('children')
        context['all_tags'] = Tag.objects.filter(status='active').order_by('name')
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        # Handle tags from the hidden input
        tags_input = self.request.POST.get('tags', '')
        if tags_input:
            tag_ids = [int(tid) for tid in tags_input.split(',') if tid.isdigit()]
            self.object.tags.set(tag_ids)
        else:
            self.object.tags.clear()
        
        return response


class PostUpdateView(BaseUpdateView):
    model = Post
    form_class = PostForm
    template_name = 'dashboard/post_form.html'
    success_url = reverse_lazy('dashboard:post_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.filter(status='active').prefetch_related('children')
        context['all_tags'] = Tag.objects.filter(status='active').order_by('name')
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Handle tags from the hidden input
        tags_input = self.request.POST.get('tags', '')
        if tags_input:
            tag_ids = [int(tid) for tid in tags_input.split(',') if tid.isdigit()]
            self.object.tags.set(tag_ids)
        else:
            self.object.tags.clear()
        
        return response


class PostDeleteView(BaseDeleteView):
    model = Post
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:post_list')


# Page Views
class PageListView(BaseListView):
    model = Page
    template_name = 'dashboard/page_list.html'
    context_object_name = 'pages'
    
    def get_queryset(self):
        return Page.objects.order_by('order', 'title')


class PageCreateView(BaseCreateView):
    model = Page
    form_class = PageForm
    template_name = 'dashboard/page_form.html'
    success_url = reverse_lazy('dashboard:page_list')


class PageUpdateView(BaseUpdateView):
    model = Page
    form_class = PageForm
    template_name = 'dashboard/page_form.html'
    success_url = reverse_lazy('dashboard:page_list')


class PageDeleteView(BaseDeleteView):
    model = Page
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:page_list')


# Category Views
class CategoryListView(BaseListView):
    model = Category
    template_name = 'dashboard/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.prefetch_related(
            'applies_to',
            'posts',
            'pages',
            'services',
            'trainings',
            'parent'
        ).annotate(post_count=Count('posts')).order_by('sort_order')


class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:category_list')


class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/category_form.html'
    success_url = reverse_lazy('dashboard:category_list')


class CategoryDeleteView(BaseDeleteView):
    model = Category
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:category_list')


# Download Views
class DownloadListView(BaseListView):
    model = Download
    template_name = 'dashboard/download_list.html'
    context_object_name = 'downloads'
    
    def get_queryset(self):
        return Download.objects.order_by('-created_at')


class DownloadCreateView(BaseCreateView):
    model = Download
    template_name = 'dashboard/download_form.html'
    fields = ['title', 'slug', 'description', 'file', 'version', 'featured_image', 'status', 'published_at']
    success_url = reverse_lazy('dashboard:download_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class DownloadUpdateView(BaseUpdateView):
    model = Download
    template_name = 'dashboard/download_form.html'
    fields = ['title', 'slug', 'description', 'file', 'version', 'featured_image', 'status', 'published_at']
    success_url = reverse_lazy('dashboard:download_list')


class DownloadDeleteView(BaseDeleteView):
    model = Download
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:download_list')


# Gallery Views
class GalleryListView(BaseListView):
    model = Gallery
    template_name = 'dashboard/gallery_list.html'
    context_object_name = 'galleries'
    
    def get_queryset(self):
        return Gallery.objects.annotate(image_count=Count('images')).order_by('sort_order')


class GalleryCreateView(BaseCreateView):
    model = Gallery
    template_name = 'dashboard/gallery_form.html'
    fields = ['name', 'slug', 'description', 'cover_image', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:gallery_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class GalleryUpdateView(BaseUpdateView):
    model = Gallery
    template_name = 'dashboard/gallery_form.html'
    fields = ['name', 'slug', 'description', 'cover_image', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:gallery_list')


class GalleryDeleteView(BaseDeleteView):
    model = Gallery
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:gallery_list')


# Gallery Image API Views
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from dashboard.models import GalleryImage


@staff_member_required
def gallery_image_upload(request):
    """Upload multiple images to a gallery"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})
    
    try:
        gallery_id = request.POST.get('gallery_id')
        gallery = get_object_or_404(Gallery, pk=gallery_id)
        images = request.FILES.getlist('images')
        
        if not images:
            return JsonResponse({'success': False, 'error': 'No images provided'})
        
        current_count = gallery.images.count()
        created_images = []
        
        for i, image_file in enumerate(images):
            image = GalleryImage.objects.create(
                gallery=gallery,
                image=image_file,
                sort_order=current_count + i
            )
            created_images.append({
                'id': image.id,
                'url': image.image.url
            })
        
        return JsonResponse({
            'success': True,
            'images': created_images,
            'count': len(created_images)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def gallery_image_reorder(request):
    """Reorder gallery images"""
    try:
        data = json.loads(request.body)
        images = data.get('images', [])
        
        for img_data in images:
            GalleryImage.objects.filter(pk=img_data['id']).update(
                sort_order=img_data['order']
            )
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def gallery_image_delete(request, pk):
    """Delete a gallery image"""
    try:
        image = get_object_or_404(GalleryImage, pk=pk)
        image.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
def gallery_image_detail(request, pk):
    """Get gallery image details"""
    try:
        image = get_object_or_404(GalleryImage, pk=pk)
        return JsonResponse({
            'success': True,
            'image': {
                'id': image.id,
                'title': image.title,
                'description': image.description,
                'alt_text': image.alt_text,
                'url': image.image.url
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def gallery_image_update(request, pk):
    """Update gallery image metadata"""
    try:
        image = get_object_or_404(GalleryImage, pk=pk)
        data = json.loads(request.body)
        
        image.title = data.get('title', image.title)
        image.description = data.get('description', image.description)
        image.alt_text = data.get('alt_text', image.alt_text)
        image.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Product Image Management
@staff_member_required
@require_POST
def product_image_upload(request):
    """Upload multiple images to a product"""
    try:
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        images = request.FILES.getlist('images')

        if not images:
            return JsonResponse({'success': False, 'error': 'No images provided'})

        current_count = product.images.count()
        created_images = []

        for i, image_file in enumerate(images):
            image = ProductImage.objects.create(
                product=product,
                image=image_file,
                sort_order=current_count + i
            )
            created_images.append({
                'id': image.id,
                'url': image.image.url
            })

        return JsonResponse({
            'success': True,
            'images': created_images,
            'count': len(created_images)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def product_image_reorder(request):
    """Reorder product images"""
    try:
        data = json.loads(request.body)
        images = data.get('images', [])

        for img_data in images:
            ProductImage.objects.filter(pk=img_data['id']).update(
                sort_order=img_data['order']
            )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def product_image_delete(request, pk):
    """Delete a product image"""
    try:
        image = get_object_or_404(ProductImage, pk=pk)
        image.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
def product_image_detail(request, pk):
    """Get product image details"""
    try:
        image = get_object_or_404(ProductImage, pk=pk)
        return JsonResponse({
            'success': True,
            'image': {
                'id': image.id,
                'title': image.title,
                'description': image.description,
                'alt_text': image.alt_text,
                'url': image.image.url
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def product_image_update(request, pk):
    """Update product image metadata"""
    try:
        image = get_object_or_404(ProductImage, pk=pk)
        data = json.loads(request.body)

        image.title = data.get('title', image.title)
        image.description = data.get('description', image.description)
        image.alt_text = data.get('alt_text', image.alt_text)
        image.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Testimonial Views
class TestimonialListView(BaseListView):
    model = Testimonial
    template_name = 'dashboard/testimonial_list.html'
    context_object_name = 'testimonials'
    
    def get_queryset(self):
        return Testimonial.objects.order_by('order')


class TestimonialCreateView(BaseCreateView):
    model = Testimonial
    template_name = 'dashboard/testimonial_form.html'
    fields = ['name', 'slug', 'position', 'company', 'avatar', 'testimonial', 'rating', 'featured', 'order', 'status']
    success_url = reverse_lazy('dashboard:testimonial_list')


class TestimonialUpdateView(BaseUpdateView):
    model = Testimonial
    template_name = 'dashboard/testimonial_form.html'
    fields = ['name', 'slug', 'position', 'company', 'avatar', 'testimonial', 'rating', 'featured', 'order', 'status']
    success_url = reverse_lazy('dashboard:testimonial_list')


class TestimonialDeleteView(BaseDeleteView):
    model = Testimonial
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:testimonial_list')


# Product Views
class ProductListView(BaseListView):
    model = Product
    template_name = 'dashboard/product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.order_by('-featured', 'sort_order')


class ProductCreateView(BaseCreateView):
    model = Product
    template_name = 'dashboard/product_form.html'
    fields = ['name', 'slug', 'description', 'excerpt', 'image', 'icon', 'category', 'price', 'featured', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:product_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(BaseUpdateView):
    model = Product
    template_name = 'dashboard/product_form.html'
    fields = ['name', 'slug', 'description', 'excerpt', 'image', 'icon', 'category', 'price', 'featured', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:product_list')


class ProductDeleteView(BaseDeleteView):
    model = Product
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:product_list')


# Carousel Views
class CarouselListView(BaseListView):
    model = Carousel
    template_name = 'dashboard/carousel_list.html'
    context_object_name = 'carousels'
    
    def get_queryset(self):
        return Carousel.objects.order_by('sort_order')


class CarouselCreateView(BaseCreateView):
    model = Carousel
    template_name = 'dashboard/carousel_form.html'
    fields = ['title', 'caption', 'image', 'link_url', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:carousel_list')


class CarouselUpdateView(BaseUpdateView):
    model = Carousel
    template_name = 'dashboard/carousel_form.html'
    fields = ['title', 'caption', 'image', 'link_url', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:carousel_list')


class CarouselDeleteView(BaseDeleteView):
    model = Carousel
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:carousel_list')


# FAQ Views
class FAQListView(BaseListView):
    model = FAQ
    template_name = 'dashboard/faq_list.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.order_by('category', 'sort_order')


class FAQCreateView(BaseCreateView):
    model = FAQ
    template_name = 'dashboard/faq_form.html'
    fields = ['question', 'answer', 'category', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:faq_list')


class FAQUpdateView(BaseUpdateView):
    model = FAQ
    template_name = 'dashboard/faq_form.html'
    fields = ['question', 'answer', 'category', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:faq_list')


class FAQDeleteView(BaseDeleteView):
    model = FAQ
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:faq_list')


# Menu Views
class MenuListView(BaseListView):
    model = Menu
    template_name = 'dashboard/menu_list.html'
    context_object_name = 'menus'
    
    def get_queryset(self):
        return Menu.objects.annotate(item_count=Count('items'))


class MenuCreateView(BaseCreateView):
    model = Menu
    template_name = 'dashboard/menu_form.html'
    fields = ['name', 'slug', 'location', 'description']
    success_url = reverse_lazy('dashboard:menu_list')


class MenuUpdateView(BaseUpdateView):
    model = Menu
    template_name = 'dashboard/menu_form.html'
    fields = ['name', 'slug', 'location', 'description']
    success_url = reverse_lazy('dashboard:menu_list')


class MenuDeleteView(BaseDeleteView):
    model = Menu
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:menu_list')


# Product Request Views
class ProductRequestListView(BaseListView):
    model = ProductRequest
    template_name = 'dashboard/product_request_list.html'
    context_object_name = 'requests'
    
    def get_queryset(self):
        return ProductRequest.objects.prefetch_related('items', 'items__product').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = ProductRequest.objects.filter(status='pending').count()
        context['processing_count'] = ProductRequest.objects.filter(status='processing').count()
        context['completed_count'] = ProductRequest.objects.filter(status='completed').count()
        return context


class ProductRequestDetailView(AdminRequiredMixin, UpdateView):
    model = ProductRequest
    template_name = 'dashboard/product_request_detail.html'
    fields = ['status', 'notes']
    
    def get_success_url(self):
        return reverse_lazy('dashboard:product_request_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Request updated successfully!')
        return super().form_valid(form)


# Service Views
class ServiceListView(BaseListView):
    model = Service
    template_name = 'dashboard/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        return Service.objects.order_by('-featured', 'sort_order')


class ServiceCreateView(BaseCreateView):
    model = Service
    template_name = 'dashboard/service_form.html'
    fields = ['name', 'slug', 'description', 'excerpt', 'image', 'icon', 'category', 'price', 'featured', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:service_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ServiceUpdateView(BaseUpdateView):
    model = Service
    template_name = 'dashboard/service_form.html'
    fields = ['name', 'slug', 'description', 'excerpt', 'image', 'icon', 'category', 'price', 'featured', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:service_list')


class ServiceDeleteView(BaseDeleteView):
    model = Service
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:service_list')


# Service Request Views
class ServiceRequestListView(BaseListView):
    model = ServiceRequest
    template_name = 'dashboard/service_request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return ServiceRequest.objects.prefetch_related('items', 'items__service').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = ServiceRequest.objects.filter(status='pending').count()
        context['processing_count'] = ServiceRequest.objects.filter(status='processing').count()
        context['completed_count'] = ServiceRequest.objects.filter(status='completed').count()
        return context


class ServiceRequestDetailView(AdminRequiredMixin, UpdateView):
    model = ServiceRequest
    template_name = 'dashboard/service_request_detail.html'
    fields = ['status', 'notes']

    def get_success_url(self):
        return reverse_lazy('dashboard:service_request_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Request updated successfully!')
        return super().form_valid(form)


# Training Views
class TrainingListView(BaseListView):
    model = Training
    template_name = 'dashboard/training_list.html'
    context_object_name = 'trainings'

    def get_queryset(self):
        return Training.objects.order_by('-featured', 'sort_order')


class TrainingCreateView(BaseCreateView):
    model = Training
    template_name = 'dashboard/training_form.html'
    fields = ['name', 'slug', 'description', 'short_description', 'excerpt', 'image', 'icon', 'category', 'duration', 'price', 'featured', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:training_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TrainingUpdateView(BaseUpdateView):
    model = Training
    template_name = 'dashboard/training_form.html'
    fields = ['name', 'slug', 'description', 'short_description', 'excerpt', 'image', 'icon', 'category', 'duration', 'price', 'featured', 'sort_order', 'status']
    success_url = reverse_lazy('dashboard:training_list')


class TrainingDeleteView(BaseDeleteView):
    model = Training
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:training_list')


# Training Request Views
class TrainingRequestListView(BaseListView):
    model = TrainingRequest
    template_name = 'dashboard/training_request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return TrainingRequest.objects.select_related('training').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = TrainingRequest.objects.filter(status='pending').count()
        context['processing_count'] = TrainingRequest.objects.filter(status='processing').count()
        context['completed_count'] = TrainingRequest.objects.filter(status='completed').count()
        return context


class TrainingRequestDetailView(AdminRequiredMixin, UpdateView):
    model = TrainingRequest
    template_name = 'dashboard/training_request_detail.html'
    fields = ['status', 'notes']

    def get_success_url(self):
        return reverse_lazy('dashboard:training_request_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Request updated successfully!')
        return super().form_valid(form)


# Consultation Views
class ConsultationListView(BaseListView):
    model = Consultation
    template_name = 'dashboard/consultation_list.html'
    context_object_name = 'consultations'

    def get_queryset(self):
        return Consultation.objects.prefetch_related('files').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_count'] = Consultation.objects.filter(status='pending').count()
        context['confirmed_count'] = Consultation.objects.filter(status='confirmed').count()
        context['completed_count'] = Consultation.objects.filter(status='completed').count()
        return context


class ConsultationDetailView(AdminRequiredMixin, UpdateView):
    model = Consultation
    template_name = 'dashboard/consultation_detail.html'
    fields = ['status', 'notes']

    def get_queryset(self):
        return Consultation.objects.prefetch_related('files')

    def get_success_url(self):
        return reverse_lazy('dashboard:consultation_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Consultation updated successfully!')
        return super().form_valid(form)


# Company Info View
class CompanyInfoUpdateView(AdminRequiredMixin, UpdateView):
    model = CompanyInfo
    template_name = 'dashboard/company_info_form.html'
    fields = [
        'company_name', 'description', 'logo', 'favicon', 'email', 'phone',
        'address', 'city', 'state', 'postal_code', 'country',
        'latitude', 'longitude',
        'facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'whatsapp',
        'anthem'
    ]
    success_url = reverse_lazy('dashboard:company_info')
    
    def get_object(self):
        return CompanyInfo.get_instance()
    
    def form_valid(self, form):
        messages.success(self.request, 'Company information updated successfully!')
        return super().form_valid(form)


# CEO Info View
class CEOInfoUpdateView(AdminRequiredMixin, UpdateView):
    model = CEOInfo
    template_name = 'dashboard/ceo_info_form.html'
    fields = [
        'name', 'title', 'bio', 'message', 'photo', 'email', 'phone',
        'social_linkedin', 'social_twitter', 'social_facebook', 'is_active'
    ]
    success_url = reverse_lazy('dashboard:ceo_info')
    
    def get_object(self):
        return CEOInfo.get_instance()
    
    def form_valid(self, form):
        messages.success(self.request, 'CEO information updated successfully!')
        return super().form_valid(form)


# User Profile View
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """User profile update view - users can only edit their own profile"""
    model = User
    template_name = 'dashboard/profile_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'bio']
    
    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('dashboard:user_profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


# User Profile View
class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """User profile update view - users can only edit their own profile"""
    model = User
    template_name = 'dashboard/profile_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'bio']
    
    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('dashboard:user_profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


# User Management Views
class UserListView(BaseListView):
    model = User
    template_name = 'dashboard/user_list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.order_by('-created_at')


# AJAX Views for Categories and Tags
from django.views.decorators.http import require_POST


@staff_member_required
@require_POST
def category_create_ajax(request):
    """Create a new category via AJAX"""
    try:
        name = request.POST.get('name', '').strip()
        parent_id = request.POST.get('parent', '').strip()
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Category name is required'})
        
        # Check if category with this name already exists
        if Category.objects.filter(name__iexact=name).exists():
            return JsonResponse({'success': False, 'error': 'A category with this name already exists'})
        
        # Create the category
        category_data = {'name': name}
        if parent_id:
            try:
                parent = Category.objects.get(pk=parent_id)
                category_data['parent'] = parent
            except Category.DoesNotExist:
                pass
        
        category = Category.objects.create(**category_data)
        
        return JsonResponse({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
                'parent_id': category.parent_id
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Video Views
class VideoListView(BaseListView):
    model = Video
    template_name = 'dashboard/video_list.html'
    context_object_name = 'videos'
    
    def get_queryset(self):
        return Video.objects.order_by('sort_order', '-created_at')


class VideoCreateView(BaseCreateView):
    model = Video
    template_name = 'dashboard/video_form.html'
    fields = ['title', 'slug', 'description', 'embed_code', 'thumbnail', 'sort_order', 'status', 'published_at']
    success_url = reverse_lazy('dashboard:video_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class VideoUpdateView(BaseUpdateView):
    model = Video
    template_name = 'dashboard/video_form.html'
    fields = ['title', 'slug', 'description', 'embed_code', 'thumbnail', 'sort_order', 'status', 'published_at']
    success_url = reverse_lazy('dashboard:video_list')


class VideoDeleteView(BaseDeleteView):
    model = Video
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:video_list')


@staff_member_required
@require_POST
def tag_create_ajax(request):
    """Create a new tag via AJAX"""
    try:
        name = request.POST.get('name', '').strip()

        if not name:
            return JsonResponse({'success': False, 'error': 'Tag name is required'})

        # Check if tag with this name already exists (case-insensitive)
        existing_tag = Tag.objects.filter(name__iexact=name).first()
        if existing_tag:
            return JsonResponse({
                'success': True,
                'tag': {
                    'id': existing_tag.id,
                    'name': existing_tag.name,
                    'slug': existing_tag.slug
                }
            })

        # Create the tag
        tag = Tag.objects.create(name=name)

        return JsonResponse({
            'success': True,
            'tag': {
                'id': tag.id,
                'name': tag.name,
                'slug': tag.slug
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Revision Management Views
class PageRevisionListView(AdminRequiredMixin, ListView):
    """List all revisions for a page"""
    model = PageRevision
    template_name = 'dashboard/page_revision_list.html'
    context_object_name = 'revisions'

    def get_queryset(self):
        self.page = get_object_or_404(Page, pk=self.kwargs['page_id'])
        return PageRevision.objects.filter(page=self.page).order_by('-revision_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.page
        return context


class PostRevisionListView(AdminRequiredMixin, ListView):
    """List all revisions for a post"""
    model = PostRevision
    template_name = 'dashboard/post_revision_list.html'
    context_object_name = 'revisions'

    def get_queryset(self):
        self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return PostRevision.objects.filter(post=self.post).order_by('-revision_number')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post
        return context


@staff_member_required
@require_POST
def restore_page_revision(request, revision_id):
    """Restore a page to a specific revision"""
    try:
        revision = get_object_or_404(PageRevision, pk=revision_id)
        revision.restore()
        messages.success(request, f'Page restored to revision {revision.revision_number} successfully!')
        return JsonResponse({'success': True, 'redirect_url': reverse_lazy('dashboard:page_list')})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_member_required
@require_POST
def restore_post_revision(request, revision_id):
    """Restore a post to a specific revision"""
    try:
        revision = get_object_or_404(PostRevision, pk=revision_id)
        revision.restore()
        messages.success(request, f'Post restored to revision {revision.revision_number} successfully!')
        return JsonResponse({'success': True, 'redirect_url': reverse_lazy('dashboard:post_list')})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# AI Configuration Views
class AIConfigurationListView(AdminRequiredMixin, ListView):
    """List all AI configurations"""
    model = AIConfiguration
    template_name = 'dashboard/ai_config_list.html'
    context_object_name = 'configs'

    def get_queryset(self):
        return AIConfiguration.objects.order_by('-created_at')


class AIConfigurationCreateView(AdminRequiredMixin, CreateView):
    """Create a new AI configuration"""
    model = AIConfiguration
    template_name = 'dashboard/ai_config_form.html'
    fields = ['name', 'model_name', 'api_endpoint', 'api_key', 'system_prompt']
    success_url = reverse_lazy('dashboard:ai_config_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'AI configuration created successfully!')
        return super().form_valid(form)


class AIConfigurationUpdateView(AdminRequiredMixin, UpdateView):
    """Update an AI configuration"""
    model = AIConfiguration
    template_name = 'dashboard/ai_config_form.html'
    fields = ['name', 'model_name', 'api_endpoint', 'api_key', 'system_prompt']
    success_url = reverse_lazy('dashboard:ai_config_list')

    def form_valid(self, form):
        messages.success(self.request, 'AI configuration updated successfully!')
        return super().form_valid(form)


class AIConfigurationDeleteView(AdminRequiredMixin, DeleteView):
    """Delete an AI configuration"""
    model = AIConfiguration
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:ai_config_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'AI configuration deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ===== EMAIL CONFIGURATION VIEWS =====

class EmailConfigurationListView(AdminRequiredMixin, ListView):
    """List all email configurations"""
    model = EmailConfiguration
    template_name = 'dashboard/email_config_list.html'
    context_object_name = 'email_configs'


class EmailConfigurationCreateView(AdminRequiredMixin, CreateView):
    """Create a new email configuration"""
    model = EmailConfiguration
    template_name = 'dashboard/email_config_form.html'
    fields = ['name', 'is_active', 'backend', 'email_host', 'email_port', 'email_use_tls',
              'email_host_user', 'email_host_password', 'from_email', 'from_name', 'admin_email', 'notes']
    success_url = reverse_lazy('dashboard:email_config_list')

    def form_valid(self, form):
        # If this is set to active, deactivate all others
        if form.cleaned_data.get('is_active'):
            EmailConfiguration.objects.update(is_active=False)
        messages.success(self.request, 'Email configuration created successfully!')
        return super().form_valid(form)


class EmailConfigurationUpdateView(AdminRequiredMixin, UpdateView):
    """Update an email configuration"""
    model = EmailConfiguration
    template_name = 'dashboard/email_config_form.html'
    fields = ['name', 'is_active', 'backend', 'email_host', 'email_port', 'email_use_tls',
              'email_host_user', 'email_host_password', 'from_email', 'from_name', 'admin_email', 'notes']
    success_url = reverse_lazy('dashboard:email_config_list')

    def form_valid(self, form):
        # If this is set to active, deactivate all others
        if form.cleaned_data.get('is_active'):
            EmailConfiguration.objects.exclude(pk=self.object.pk).update(is_active=False)
        messages.success(self.request, 'Email configuration updated successfully!')
        return super().form_valid(form)


class EmailConfigurationDeleteView(AdminRequiredMixin, DeleteView):
    """Delete an email configuration"""
    model = EmailConfiguration
    template_name = 'dashboard/confirm_delete.html'
    success_url = reverse_lazy('dashboard:email_config_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Email configuration deleted successfully!')
        return super().delete(request, *args, **kwargs)


# AI Content Generation API
@staff_member_required
def generate_content_with_ai(request):
    """Generate content using DeepSeek AI with streaming support"""
    import json
    import logging
    from django.http import StreamingHttpResponse
    from openai import OpenAI

    logger = logging.getLogger(__name__)

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method is allowed'})

    try:
        # Get active AI configuration
        ai_config = AIConfiguration.get_active()
        if not ai_config:
            logger.error("No active AI configuration found")
            return JsonResponse({
                'success': False,
                'error': 'No active AI configuration found. Please activate an AI configuration first.'
            })

        logger.info(f"Using AI config: {ai_config.name} (model: {ai_config.model_name})")

        # Get request data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in request body: {e}")
            return JsonResponse({'success': False, 'error': 'Invalid JSON in request body'})

        prompt = data.get('prompt', '').strip()
        action = data.get('action', 'generate')  # generate, replace, edit
        current_content = data.get('current_content', '')

        if not prompt:
            return JsonResponse({'success': False, 'error': 'Prompt is required'})

        logger.info(f"AI generation request - Action: {action}, Prompt length: {len(prompt)}")

        # Prepare messages based on action
        messages = []

        # Add system prompt if configured
        system_prompt = ai_config.system_prompt or "You are a helpful AI assistant that generates high-quality content."
        # Enhance system prompt for better code generation
        enhanced_system_prompt = system_prompt + """

When generating HTML, CSS, or JavaScript code:
- Always wrap the code in markdown code blocks with the appropriate language identifier (e.g., ```html, ```css, ```javascript)
- Include the complete, working code - never truncate or use placeholders like "// insert code here"
- Make sure the code is properly formatted and indented
- For HTML, include proper DOCTYPE, html, head, and body tags if generating a complete page
- For CSS, include complete rules with proper selectors and properties
- Always complete the code block with closing ``` markers

When generating regular text content (not code):
- Write naturally without markdown code blocks
- Use proper formatting with paragraphs, headings, and lists as needed
- Never wrap regular content in ```code blocks"""

        messages.append({
            'role': 'system',
            'content': enhanced_system_prompt
        })

        # Prepare user prompt based on action
        user_prompt = prompt
        if action == 'edit' and current_content:
            user_prompt = f"{prompt}\n\nCurrent content:\n{current_content}\n\nPlease improve the above content based on my instructions."
        elif action == 'generate':
            # Add instruction for clarity
            if any(keyword in prompt.lower() for keyword in ['html', 'css', 'javascript', 'code', 'component', 'button', 'form', 'layout']):
                user_prompt = f"{prompt}\n\nPlease provide the complete code in a markdown code block. Ensure all code is complete and functional."

        messages.append({
            'role': 'user',
            'content': user_prompt
        })

        # Create OpenAI client with configured endpoint
        try:
            client = OpenAI(
                api_key=ai_config.api_key,
                base_url=ai_config.api_endpoint
            )
            logger.info(f"OpenAI client created with endpoint: {ai_config.api_endpoint}")
        except Exception as e:
            logger.error(f"Failed to create OpenAI client: {e}")
            return JsonResponse({'success': False, 'error': f'Failed to initialize AI client: {str(e)}'})

        logger.info(f"About to create generator function")

        def generate():
            """Generator function for streaming response"""
            logger.info(f"Generator function called, starting AI generation")
            try:
                logger.info(f"Attempting to create stream with model: {ai_config.model_name}")
                stream = client.chat.completions.create(
                    model=ai_config.model_name,
                    messages=messages,
                    max_tokens=4000,
                    temperature=0.7,
                    stream=True
                )
                logger.info("Stream object created successfully, starting to iterate")

                # Stream the response
                chunk_count = 0
                for chunk in stream:
                    chunk_count += 1
                    logger.debug(f"Received chunk #{chunk_count}")

                    if chunk.choices and len(chunk.choices) > 0:
                        delta = chunk.choices[0].delta
                        if hasattr(delta, 'content') and delta.content is not None:
                            content = delta.content
                            logger.debug(f"Sending content chunk: {len(content)} chars")
                            yield f"data: {json.dumps({'content': content})}\n\n"

                # Send completion signal
                logger.info(f"AI generation completed successfully after {chunk_count} chunks")
                yield f"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                logger.error(f"Error during AI streaming: {type(e).__name__}: {str(e)}", exc_info=True)
                error_msg = str(e)
                # Include more details for common errors
                if 'timeout' in str(e).lower():
                    error_msg = "The AI request timed out. Please try again with a shorter prompt."
                elif 'connection' in str(e).lower():
                    error_msg = "Could not connect to AI service. Please check your API configuration."
                elif 'key' in str(e).lower() or 'auth' in str(e).lower():
                    error_msg = "Authentication failed. Please check your API key."
                elif 'model' in str(e).lower():
                    error_msg = f"Model '{ai_config.model_name}' not found. Please check your AI configuration."
                yield f"data: {json.dumps({'error': error_msg})}\n\n"

        logger.info(f"About to create StreamingHttpResponse")
        try:
            response = StreamingHttpResponse(generate(), content_type='text/event-stream')
            response['X-Accel-Buffering'] = 'no'
            response['Cache-Control'] = 'no-cache, no-transform'
            logger.info(f"StreamingHttpResponse created successfully, about to return")
            return response
        except Exception as e:
            logger.error(f"Failed to create StreamingHttpResponse: {type(e).__name__}: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'error': f'Failed to create streaming response: {str(e)}'})

    except Exception as e:
        logger.error(f"Unexpected error in generate_content_with_ai: {e}", exc_info=True)
        return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'})


# Bulk Delete View
@require_POST
@staff_member_required
def bulk_delete(request):
    """Bulk delete items based on model type and IDs"""
    model_name = request.POST.get('model')
    item_ids = request.POST.getlist('ids', [])
    
    if not model_name or not item_ids:
        messages.error(request, 'No items selected for deletion.')
        return redirect(request.META.get('HTTP_REFERER', '/dashboard/'))
    
    # Map model names to actual models
    model_map = {
        'post': Post,
        'page': Page,
        'category': Category,
        'tag': Tag,
        'product': Product,
        'service': Service,
        'training': Training,
        'gallery': Gallery,
        'testimonial': Testimonial,
        'faq': FAQ,
        'video': Video,
        'download': Download,
        'carousel': Carousel,
        'menu': Menu,
        'product_request': ProductRequest,
        'service_request': ServiceRequest,
        'training_request': TrainingRequest,
        'consultation': Consultation,
    }
    
    model_class = model_map.get(model_name)
    if not model_class:
        messages.error(request, 'Invalid model type.')
        return redirect(request.META.get('HTTP_REFERER', '/dashboard/'))
    
    try:
        queryset = model_class.objects.filter(pk__in=item_ids)
        count = queryset.count()
        queryset.delete()
        messages.success(request, f'Successfully deleted {count} item(s).')
    except Exception as e:
        messages.error(request, f'Error deleting items: {str(e)}')
    
    return redirect(request.META.get('HTTP_REFERER', '/dashboard/'))

from django.shortcuts import render, get_object_or_404
from .models import Service, ServiceCategory


def category_list(request):
    """Display all service categories"""
    categories = ServiceCategory.objects.filter(
        status='active'
    ).prefetch_related('services__service').all()

    context = {
        'categories': categories,
    }
    return render(request, 'services/category_list.html', context)


def category_detail(request, slug):
    """Display all services in a category"""
    category = get_object_or_404(
        ServiceCategory,
        slug=slug,
        status='active'
    )

    services = category.services.filter(
        status='published'
    ).order_by('sort_order', 'title')

    context = {
        'category': category,
        'services': services,
    }
    return render(request, 'services/category_detail.html', context)


def detail(request, slug):
    """Display individual service details"""
    service = get_object_or_404(
        Service,
        slug=slug,
        status='published'
    )

    # Get related services from the same category
    related_services = Service.objects.filter(
        category=service.category,
        status='published'
    ).exclude(id=service.id)[:4]

    context = {
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'services/detail.html', context)

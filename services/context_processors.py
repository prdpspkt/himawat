from .models import ServiceCategory


def service_categories(request):
    """
    Context processor to make service categories available in all templates.
    """
    return {
        'service_categories': ServiceCategory.objects.filter(
            status='active'
        ).prefetch_related('services__service').order_by('sort_order', 'name')
    }

from dashboard.models import Menu, CompanyInfo, Carousel, Testimonial, FAQ, CEOInfo, Gallery, Product


def site_context(request):
    """Context processor to add site-wide data to all templates"""
    context = {}
    
    # Company info
    try:
        context['company_info'] = CompanyInfo.get_instance()
    except:
        context['company_info'] = None
    
    # CEO info
    try:
        ceo = CEOInfo.get_instance()
        context['ceo_info'] = ceo if ceo.is_active else None
    except:
        context['ceo_info'] = None
    
    # Main navigation menu
    try:
        # Try to find by location first, more flexible
        main_menu = Menu.objects.filter(location='main').first()
        if not main_menu:
            # Fallback to any menu if no main menu exists
            main_menu = Menu.objects.first()
        if main_menu:
            context['main_menu'] = main_menu.items.filter(is_active=True, parent=None).prefetch_related('children')
    except:
        context['main_menu'] = []

    # Top menu
    try:
        top_menu = Menu.objects.filter(location='top-bar').first()
        if top_menu:
            context['top_menu'] = top_menu.items.filter(is_active=True, parent=None)
        else:
            context['top_menu'] = []
    except:
        context['top_menu'] = []

    # Footer menus
    try:
        footer_menu1 = Menu.objects.filter(location='footer-1').first()
        if footer_menu1:
            context['footer_menu1'] = footer_menu1.items.filter(is_active=True, parent=None)
        else:
            context['footer_menu1'] = []
    except:
        context['footer_menu1'] = []

    try:
        footer_menu2 = Menu.objects.filter(location='footer-2').first()
        if footer_menu2:
            context['footer_menu2'] = footer_menu2.items.filter(is_active=True, parent=None)
        else:
            context['footer_menu2'] = []
    except:
        context['footer_menu2'] = []
    
    return context


def home_context(request):
    """Context processor for homepage-specific data"""
    context = {}
    
    # Carousel slides
    try:
        context['carousel_slides'] = Carousel.objects.filter(status='active').order_by('sort_order')
    except:
        context['carousel_slides'] = []
    
    # Featured testimonials
    try:
        context['featured_testimonials'] = Testimonial.objects.filter(
            status='published', 
            featured=True
        ).order_by('order')[:3]
    except:
        context['featured_testimonials'] = []
    
    # FAQs grouped by category
    try:
        vastu_faqs = FAQ.objects.filter(category='vastu', status='active').order_by('sort_order')
        engineering_faqs = FAQ.objects.filter(category='engineering', status='active').order_by('sort_order')
        context['faqs'] = {
            'vastu': vastu_faqs,
            'engineering': engineering_faqs
        }
    except:
        context['faqs'] = {'vastu': [], 'engineering': []}
    
    return context


def page_context(request):
    """Context processor for page templates with dynamic content"""
    context = {}
    
    # Galleries for gallery page template
    try:
        context['galleries'] = Gallery.objects.filter(
            status='active'
        ).prefetch_related('images').order_by('sort_order')
    except:
        context['galleries'] = []
    
    # Products for product page template
    try:
        products = Product.objects.filter(status='active').order_by('-featured', 'sort_order')
        
        # Filter by category if specified
        category = request.GET.get('category')
        if category:
            products = products.filter(category=category)
        
        context['products'] = products
    except:
        context['products'] = []
    
    return context

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.text import slugify
import json

User = get_user_model()


class TimestampModel(models.Model):
    """Abstract base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimestampModel):
    """Unified categories for Posts, Pages, Services, and Trainings"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    CONTENT_TYPE_CHOICES = [
        ('posts', 'Posts'),
        ('pages', 'Pages'),
        ('products', 'Products'),
        ('services', 'Services'),
        ('trainings', 'Trainings'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    template_name = models.CharField(max_length=255, blank=True, help_text="Custom template path (e.g., 'cms/categories/services-category.html'). Leave empty for auto-detection.")

    # Choose which content types this category applies to
    applies_to = models.ManyToManyField(
        ContentType,
        blank=True,
        related_name='categories',
        help_text="Select which content types this category applies to",
        limit_choices_to={'model__in': ['post', 'page', 'product', 'service', 'training']}
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:category_detail', kwargs={'slug': self.slug})

    def get_applies_to_display(self):
        """Get display names of content types this category applies to"""
        return [ct.model for ct in self.applies_to.all()]

    def get_template(self):
        """
        Get the template for this category with priority:
        1. Custom template_name field (manually assigned)
        2. Slug-based template (e.g., 'cms/categories/services-category.html')
        3. Default template (e.g., 'cms/categories/category.html')
        """
        from django.template.loader import select_template

        # Priority 1: Custom template_name (manually assigned - highest priority)
        if self.template_name:
            return self.template_name

        # Priority 2: Slug-based template (auto-discovery based on slug)
        slug_template = f'cms/categories/{self.slug}-category.html'

        # Try to load the slug-based template
        try:
            template = select_template([slug_template])
            # If no exception, the template exists
            return slug_template
        except:
            # Template doesn't exist, fall through to default
            pass

        # Priority 3: Default template
        return 'cms/categories/category.html'


class Tag(TimestampModel):
    """Blog post tags"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(TimestampModel):
    """Blog posts"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='posts/', null=True, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    custom_fields = models.JSONField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    view_count = models.PositiveIntegerField(default=0)
    allow_comments = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    template_name = models.CharField(max_length=255, blank=True, help_text="Custom template path (e.g., 'cms/posts/services-post.html'). Leave empty for auto-detection.")

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:post_detail', kwargs={'slug': self.slug})

    def get_template(self):
        """
        Get the template for this post with priority:
        1. Custom template_name field (manually assigned)
        2. Slug-based template (e.g., 'cms/posts/services-post.html')
        3. Default template (e.g., 'cms/posts/post.html')
        """
        from django.template.loader import select_template

        # Priority 1: Custom template_name (manually assigned - highest priority)
        if self.template_name:
            return self.template_name

        # Priority 2: Slug-based template (auto-discovery based on slug)
        slug_template = f'cms/posts/{self.slug}-post.html'
        templates_to_try = [slug_template, 'cms/posts/post.html']

        # select_template returns the first template that exists
        try:
            template = select_template(templates_to_try)
            # Return the slug template if it exists, otherwise default
            if template.name == slug_template:
                return slug_template
        except:
            pass

        # Priority 3: Default template
        return 'cms/posts/post.html'


class Page(TimestampModel):
    """CMS Pages"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    TEMPLATE_CHOICES = [
        ('default', 'Default'),
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('contact', 'Contact Page'),
        ('full_width', 'Full Width'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to='pages/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='pages')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    template = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='default', blank=True, help_text="Preset template or leave empty for custom template")
    template_name = models.CharField(max_length=255, blank=True, help_text="Custom template path (e.g., 'cms/pages/services-page.html'). Overrides preset template if specified.")
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    blocks = models.JSONField(null=True, blank=True, help_text="Page builder blocks")

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:page_detail', kwargs={'slug': self.slug})

    def get_template(self):
        """
        Get the template for this page with priority:
        1. Custom template_name field (manually assigned - highest priority)
        2. Preset template field (e.g., 'home', 'about', etc.)
        3. Slug-based template (e.g., 'cms/pages/services-page.html')
        4. Default template (e.g., 'cms/pages/default.html')
        """
        from django.template.loader import select_template

        # Priority 1: Custom template_name (manually assigned - highest priority)
        if self.template_name:
            return self.template_name

        # Priority 2: Use preset template if specified
        if self.template and self.template != 'default':
            template_map = {
                'home': 'cms/home.html',
                'about': 'cms/pages/about.html',
                'contact': 'cms/pages/contact.html',
                'full_width': 'cms/pages/full_width.html',
            }
            if self.template in template_map:
                return template_map[self.template]

        # Priority 3: Slug-based template (auto-discovery based on slug)
        slug_template = f'cms/pages/{self.slug}-page.html'
        templates_to_try = [slug_template, 'cms/pages/default.html']

        # select_template returns the first template that exists
        try:
            template = select_template(templates_to_try)
            # Return the slug template if it exists, otherwise default
            if template.name == slug_template:
                return slug_template
        except:
            pass

        # Priority 4: Default template
        return 'cms/pages/default.html'


class Download(TimestampModel):
    """File downloads"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='downloads/')
    file_size = models.PositiveIntegerField(default=0)
    file_type = models.CharField(max_length=100, blank=True)
    version = models.CharField(max_length=50, blank=True)
    download_count = models.PositiveIntegerField(default=0)
    featured_image = models.ImageField(upload_to='downloads/images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.file.name.split('.')[-1] if '.' in self.file.name else ''
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:download_detail', kwargs={'slug': self.slug})


class Gallery(TimestampModel):
    """Photo galleries"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='galleries/covers/', null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Galleries'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:gallery_detail', kwargs={'slug': self.slug})


class GalleryImage(TimestampModel):
    """Images within galleries"""
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='galleries/images/')
    thumbnail = models.ImageField(upload_to='galleries/thumbnails/', null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return self.title or f"Image {self.id}"


class Testimonial(TimestampModel):
    """Customer testimonials"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    position = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='testimonials/avatars/', null=True, blank=True)
    testimonial = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    video_url = models.URLField(blank=True)
    video = models.FileField(upload_to='testimonials/videos/', null=True, blank=True, help_text="Upload a video file (MP4, WebM, etc.)")
    website = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Carousel(TimestampModel):
    """Homepage carousel slides"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True)
    image = models.ImageField(upload_to='carousel/')
    link_url = models.URLField(blank=True)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name_plural = 'Carousels'
        ordering = ['sort_order', 'created_at']

    def __str__(self):
        return self.title


class FAQ(TimestampModel):
    """Frequently Asked Questions"""
    CATEGORY_CHOICES = [
        ('vastu', 'Vastu'),
        ('engineering', 'Engineering'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='vastu')
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['category', 'sort_order']

    def __str__(self):
        return self.question


class Product(TimestampModel):
    """Products"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-featured', 'sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:product_detail', kwargs={'slug': self.slug})


class ProductImage(TimestampModel):
    """Additional product images"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    thumbnail = models.ImageField(upload_to='products/thumbnails/', null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_primary', 'sort_order']

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductRequest(TimestampModel):
    """Product inquiries/requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    captcha_token = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request #{self.id} by {self.name}"

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class ProductRequestItem(TimestampModel):
    """Individual items in a product request (shopping cart style)"""
    request = models.ForeignKey(ProductRequest, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='request_items')
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, help_text="Specific requirements for this item")

    class Meta:
        ordering = ['created_at']
        unique_together = ['request', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Request #{self.request.id})"


class Consultation(TimestampModel):
    """Consultation bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=255)
    service_type = models.CharField(max_length=50, blank=True, help_text='Comma-separated: onsite, online')
    message = models.TextField()
    preferred_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    captcha_token = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Consultation: {self.subject} by {self.name}"


class ConsultationFile(TimestampModel):
    """Files attached to consultation requests"""
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='consultations/files/%Y/%m/')
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100, blank=True)
    file_size = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.filename

    def save(self, *args, **kwargs):
        if self.file:
            self.filename = self.file.name
            self.file_type = self.file.name.split('.')[-1] if '.' in self.file.name else ''
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class Contact(TimestampModel):
    """Contact form submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, help_text='Internal notes about this contact')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return f"Contact: {self.subject} by {self.name}"


class Menu(TimestampModel):
    """Navigation menus"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=100, blank=True, help_text="e.g., main, footer")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItem(TimestampModel):
    """Individual menu items"""
    TYPE_CHOICES = [
        ('page', 'Page'),
        ('custom_link', 'Custom Link'),
        ('category', 'Category'),
        ('post', 'Post'),
        ('divider', 'Divider'),
    ]

    TARGET_CHOICES = [
        ('_self', 'Same Window'),
        ('_blank', 'New Window'),
    ]

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='custom_link')
    url = models.CharField(max_length=500, blank=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-home', 'fas fa-user')")
    order = models.IntegerField(default=0)
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default='_self')
    css_class = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

    def get_url(self):
        if self.type == 'page' and self.page:
            return self.page.get_absolute_url()
        return self.url

    def clean_url(self):
        """Ensure URL has proper format for custom links"""
        if self.type == 'custom_link' and self.url:
            # Don't modify if it's already a full URL or special URL
            if self.url.startswith(('http://', 'https://', 'mailto:', 'tel:', '/')):
                return self.url
            # Add https:// prefix for external URLs without protocol
            if '.' in self.url and not self.url.startswith('/'):
                return 'https://' + self.url
        return self.url

    def save(self, *args, **kwargs):
        self.url = self.clean_url()
        super().save(*args, **kwargs)


class CEOInfo(models.Model):
    """CEO/Founder information - Singleton model"""
    name = models.CharField(max_length=255, default='CEO Name')
    title = models.CharField(max_length=255, default='Founder & CEO', blank=True)
    bio = models.TextField(blank=True, help_text="Short biography of the CEO")
    message = models.TextField(blank=True, help_text="Welcome message from CEO")
    photo = models.ImageField(upload_to='ceo/', null=True, blank=True, help_text="CEO Photo (recommended: 400x400px)")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    social_linkedin = models.URLField('LinkedIn', blank=True)
    social_twitter = models.URLField('Twitter', blank=True)
    social_facebook = models.URLField('Facebook', blank=True)
    is_active = models.BooleanField(default=True, help_text="Display CEO info on frontend")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'CEO Info'
        verbose_name_plural = 'CEO Info'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and CEOInfo.objects.exists():
            existing = CEOInfo.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(pk=1, defaults={'name': 'CEO Name'})
        return instance


class Video(TimestampModel):
    """Embedded videos for media section"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, help_text="Short description of the video")
    embed_code = models.TextField(help_text="Paste the video embedding code (YouTube, Vimeo, etc.)")
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', null=True, blank=True, help_text="Optional custom thumbnail")
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:video_detail', kwargs={'slug': self.slug})


class CompanyInfo(models.Model):
    """Company information/singleton model"""
    company_name = models.CharField(max_length=255, default='Himwatkhanda Vastu Pvt. Ltd.')
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company/', null=True, blank=True)
    favicon = models.ImageField(upload_to='company/', null=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Nepal')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    anthem = models.FileField(upload_to='company/anthem/', null=True, blank=True, help_text="Company anthem MP3 file")
    google_analytics_id = models.CharField(max_length=50, blank=True, help_text="Google Analytics Tracking ID (e.g., G-XXXXXXXXXX)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="Default meta keywords for all pages (can be overridden per page)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company Info'
        verbose_name_plural = 'Company Info'

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and CompanyInfo.objects.exists():
            existing = CompanyInfo.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(pk=1)
        return instance


# ===== REVISION MODELS =====

class PageRevision(TimestampModel):
    """Page revision history for tracking content changes"""
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='revisions')
    revision_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    template = models.CharField(max_length=50, blank=True)
    blocks = models.JSONField(null=True, blank=True)
    revision_reason = models.TextField(blank=True, help_text="Why was this revision created?")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='page_revisions')
    is_auto_save = models.BooleanField(default=False, help_text="True for auto-saves, False for manual saves")

    class Meta:
        ordering = ['-revision_number', '-created_at']
        verbose_name = 'Page Revision'
        verbose_name_plural = 'Page Revisions'
        unique_together = ['page', 'revision_number']

    def __str__(self):
        return f"Revision {self.revision_number} of {self.page.title}"

    def restore(self):
        """Restore this revision to the page"""
        self.page.title = self.title
        self.page.content = self.content
        self.page.excerpt = self.excerpt
        self.page.meta_title = self.meta_title
        self.page.meta_description = self.meta_description
        self.page.meta_keywords = self.meta_keywords
        self.page.template = self.template
        self.page.blocks = self.blocks
        self.page.save()


class PostRevision(TimestampModel):
    """Post revision history for tracking content changes"""
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='revisions')
    revision_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    status = models.CharField(max_length=20, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    revision_reason = models.TextField(blank=True, help_text="Why was this revision created?")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='post_revisions')
    is_auto_save = models.BooleanField(default=False, help_text="True for auto-saves, False for manual saves")

    class Meta:
        ordering = ['-revision_number', '-created_at']
        verbose_name = 'Post Revision'
        verbose_name_plural = 'Post Revisions'
        unique_together = ['post', 'revision_number']

    def __str__(self):
        return f"Revision {self.revision_number} of {self.post.title}"

    def restore(self):
        """Restore this revision to the post"""
        self.post.title = self.title
        self.post.content = self.content
        self.post.excerpt = self.excerpt
        self.post.status = self.status
        self.post.published_at = self.published_at
        self.post.save()


# ===== AI CONFIGURATION MODEL =====

class AIConfiguration(TimestampModel):
    """AI service configurations for content generation"""

    name = models.CharField(max_length=255, help_text="Friendly name for this configuration")
    model_name = models.CharField(max_length=100, default='glm-4.5', help_text="Model name (e.g., glm-4.5, deepseek-chat, gpt-4)")
    api_endpoint = models.CharField(max_length=500, default='https://api.z.ai/api/paas/v4/', help_text="API endpoint URL")
    api_key = models.CharField(max_length=500, help_text="API key")
    system_prompt = models.TextField(blank=True, help_text="System prompt to guide AI behavior")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_configs')

    class Meta:
        verbose_name = 'AI Configuration'
        verbose_name_plural = 'AI Configurations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.model_name})"

    @classmethod
    def get_active(cls):
        """Get the first available AI configuration"""
        return cls.objects.first()


class EmailConfiguration(TimestampModel):
    """Email configuration for sending emails system-wide"""

    BACKEND_CHOICES = [
        ('console', 'Console (Development)'),
        ('smtp', 'SMTP (Production)'),
    ]

    name = models.CharField(max_length=255, default='Default Email Configuration', help_text="Friendly name for this configuration")
    is_active = models.BooleanField(default=True, help_text="Use this configuration as the default")
    backend = models.CharField(max_length=20, choices=BACKEND_CHOICES, default='console', help_text="Email backend to use")

    # SMTP Settings
    email_host = models.CharField(max_length=255, blank=True, default='smtp.gmail.com', help_text="SMTP server hostname")
    email_port = models.IntegerField(default=587, help_text="SMTP server port")
    email_use_tls = models.BooleanField(default=True, help_text="Use TLS for encryption")
    email_host_user = models.EmailField(blank=True, default='', help_text="SMTP username (usually email address)")
    email_host_password = models.CharField(max_length=255, blank=True, default='', help_text="SMTP password or app password")

    # From Email
    from_email = models.EmailField(blank=True, default='noreply@localhost', help_text="Default from email address")
    from_name = models.CharField(max_length=255, blank=True, default='Himwatkhanda Vastu', help_text="Sender display name")

    # Admin Email
    admin_email = models.EmailField(blank=True, default='admin@localhost', help_text="Admin email for notifications")

    notes = models.TextField(blank=True, help_text="Additional notes about this configuration")

    class Meta:
        verbose_name = 'Email Configuration'
        verbose_name_plural = 'Email Configurations'
        ordering = ['-is_active', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_backend_display()})"

    @classmethod
    def get_active(cls):
        """Get the active email configuration"""
        try:
            return cls.objects.filter(is_active=True).first()
        except:
            return None

    def apply_to_settings(self):
        """Apply this configuration to Django settings"""
        settings_dict = {
            'EMAIL_BACKEND': f"django.core.mail.backends.{self.backend}.EmailBackend",
            'DEFAULT_FROM_EMAIL': self.from_email,
            'SERVER_EMAIL': self.admin_email,
        }

        if self.backend == 'smtp':
            settings_dict.update({
                'EMAIL_HOST': self.email_host,
                'EMAIL_PORT': self.email_port,
                'EMAIL_USE_TLS': self.email_use_tls,
                'EMAIL_HOST_USER': self.email_host_user,
                'EMAIL_HOST_PASSWORD': self.email_host_password,
            })

        return settings_dict


# ===== SERVICE MODEL =====

class Service(TimestampModel):
    """Services offered by the company"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    excerpt = models.TextField(blank=True, help_text="Brief summary for listing pages")
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-home')")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='services')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Starting price or leave empty")
    featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-featured', 'sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:service_detail', kwargs={'slug': self.slug})


class ServiceRequest(TimestampModel):
    """Service inquiries/requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request #{self.id} by {self.name} for {self.service.name}"


# ===== TRAINING MODEL =====

class Training(TimestampModel):
    """Training courses offered by the company"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    excerpt = models.TextField(blank=True, help_text="Brief summary for listing pages")
    image = models.ImageField(upload_to='trainings/', null=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-graduation-cap')")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainings')
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., '5 days', '2 weeks'")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Training fee or leave empty")
    featured = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-featured', 'sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:training_detail', kwargs={'slug': self.slug})


class TrainingRequest(TimestampModel):
    """Training inquiries/requests"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='requests')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request #{self.id} by {self.name} for {self.training.name}"

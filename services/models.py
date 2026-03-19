from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class TimestampModel(models.Model):
    """Abstract base model with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ServiceCategory(TimestampModel):
    """Categories for organizing services"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-home')")
    image = models.ImageField(upload_to='service-categories/', null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        verbose_name_plural = 'Service Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:category_detail', kwargs={'slug': self.slug})


class Service(TimestampModel):
    """Service items"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        limit_choices_to={'status': 'active'}
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    short_description = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class (e.g., 'fas fa-home')")
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    featured_image = models.ImageField(upload_to='services/featured/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Starting price")
    price_display = models.CharField(max_length=100, blank=True, help_text="e.g., 'Starting from NPR 50,000'")
    sort_order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False, help_text="Show in featured services section")
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Services'
        ordering = ['sort_order', 'title']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

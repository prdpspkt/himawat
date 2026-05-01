from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from dashboard.models import (
    Category, Download, Gallery, Page, Post, Product, Service, Training, Video,
)


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'

    pages = [
        ('pages:home', 1.0),
        ('pages:product_list', 0.8),
        ('pages:service_list', 0.8),
        ('pages:training_list', 0.7),
        ('pages:post_list', 0.7),
        ('pages:download_list', 0.6),
        ('pages:gallery_list', 0.6),
        ('pages:video_list', 0.6),
        ('pages:testimonial_list', 0.5),
        ('pages:faq_list', 0.5),
        ('pages:consultation', 0.5),
        ('pages:ceo_profile', 0.4),
        ('pages:contact', 0.4),
        ('pages:tools', 0.4),
    ]

    def items(self):
        return self.pages

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Post.objects.filter(status='published').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class PageSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Page.objects.filter(status='active').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Category.objects.filter(status='active').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Product.objects.filter(status='active').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class ServiceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Service.objects.filter(status='active').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class TrainingSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Training.objects.filter(status='active').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class DownloadSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Download.objects.filter(status='published').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class GallerySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Gallery.objects.filter(status='active').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class VideoSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Video.objects.filter(status='published').order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostSitemap,
    'pages': PageSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'services': ServiceSitemap,
    'trainings': TrainingSitemap,
    'downloads': DownloadSitemap,
    'galleries': GallerySitemap,
    'videos': VideoSitemap,
}

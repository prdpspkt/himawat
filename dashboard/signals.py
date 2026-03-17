from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Page, Post, PageRevision, PostRevision


@receiver(post_save, sender=Page)
def create_page_revision(sender, instance, created, **kwargs):
    """
    Automatically create a revision when a page is saved.
    """
    # Get the current revision number for this page
    latest_revision = PageRevision.objects.filter(page=instance).order_by('-revision_number').first()
    next_revision_number = 1 if not latest_revision else latest_revision.revision_number + 1

    # Create the revision
    PageRevision.objects.create(
        page=instance,
        revision_number=next_revision_number,
        title=instance.title,
        content=instance.content,
        excerpt=instance.excerpt or '',
        meta_title=instance.meta_title or '',
        meta_description=instance.meta_description or '',
        meta_keywords=instance.meta_keywords or '',
        template=instance.template or '',
        blocks=instance.blocks,
        revision_reason='Automatic revision on save',
        is_auto_save=True
    )


@receiver(post_save, sender=Post)
def create_post_revision(sender, instance, created, **kwargs):
    """
    Automatically create a revision when a post is saved.
    """
    # Get the current revision number for this post
    latest_revision = PostRevision.objects.filter(post=instance).order_by('-revision_number').first()
    next_revision_number = 1 if not latest_revision else latest_revision.revision_number + 1

    # Create the revision
    PostRevision.objects.create(
        post=instance,
        revision_number=next_revision_number,
        title=instance.title,
        content=instance.content,
        excerpt=instance.excerpt or '',
        status=instance.status or '',
        published_at=instance.published_at,
        revision_reason='Automatic revision on save',
        is_auto_save=True
    )

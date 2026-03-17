from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dashboard.models import Page

User = get_user_model()


class Command(BaseCommand):
    help = 'Redesign ALL pages with professional web design'

    def handle(self, *args, **options):
        self.stdout.write('Redesigning all pages with professional web design...')

        # Get or create a user
        user = User.objects.filter(is_staff=True).first()
        if not user:
            user = User.objects.first()

        # Import all page designs from a separate file to keep code organized
        from .page_designs import ALL_PAGE_DESIGNS

        # Update all pages
        for slug, page_data in ALL_PAGE_DESIGNS.items():
            try:
                page = Page.objects.get(slug=slug)
                page.content = page_data['content']
                page.meta_title = page_data.get('meta_title', page.title)
                page.meta_description = page_data.get('meta_description', '')
                page.save()
                self.stdout.write(f'  ✓ Redesigned: {page.title}')
            except Page.DoesNotExist:
                self.stdout.write(f'  ✗ Not found: {slug}')

        self.stdout.write(self.style.SUCCESS('\\nAll pages redesigned successfully!'))
        self.stdout.write('\\nDesign Features Added:')
        self.stdout.write('  • Hero sections with gradients')
        self.stdout.write('  • Professional card layouts')
        self.stdout.write('  • SVG icons and illustrations')
        self.stdout.write('  • Feature grids and lists')
        self.stdout.write('  • CTA sections')
        self.stdout.write('  • Responsive designs')
        self.stdout.write('  • Modern color schemes')

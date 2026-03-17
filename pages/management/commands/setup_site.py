from django.core.management.base import BaseCommand
from dashboard.models import CompanyInfo, Menu, MenuItem, Page


class Command(BaseCommand):
    help = 'Set up initial site data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial site data...')
        
        # Create company info
        company, created = CompanyInfo.objects.get_or_create(
            pk=1,
            defaults={
                'company_name': 'Himwatkhanda Vastu Pvt. Ltd.',
                'description': 'Your Blueprint for Harmony, Structure, and Expertise. Expert Vastu consultancy, construction services, and professional training.',
                'email': 'info@himwatkhanda.com',
                'phone': '+977-98XXXXXXXX',
                'address': 'Kathmandu',
                'city': 'Kathmandu',
                'country': 'Nepal',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created company info: {company.company_name}'))
        else:
            self.stdout.write(self.style.WARNING('Company info already exists'))
        
        # Create main menu
        main_menu, created = Menu.objects.get_or_create(
            slug='main-menu',
            defaults={
                'name': 'Main Menu',
                'location': 'main',
                'description': 'Primary navigation menu'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created menu: {main_menu.name}'))
            
            # Create menu items
            menu_items = [
                {'title': 'Home', 'type': 'custom_link', 'url': '/', 'order': 1},
                {'title': 'Blog', 'type': 'custom_link', 'url': '/blog/', 'order': 2},
                {'title': 'Products', 'type': 'custom_link', 'url': '/products/', 'order': 3},
                {'title': 'Gallery', 'type': 'custom_link', 'url': '/galleries/', 'order': 4},
                {'title': 'Testimonials', 'type': 'custom_link', 'url': '/testimonials/', 'order': 5},
                {'title': 'Contact', 'type': 'custom_link', 'url': '/consultation/', 'order': 6},
            ]
            
            for item_data in menu_items:
                MenuItem.objects.create(menu=main_menu, **item_data)
            self.stdout.write(self.style.SUCCESS(f'Created {len(menu_items)} menu items'))
        else:
            self.stdout.write(self.style.WARNING('Main menu already exists'))
        
        # Create home page
        home_page, created = Page.objects.get_or_create(
            slug='home',
            defaults={
                'title': 'Home',
                'content': '<p>Welcome to Himwatkhanda Vastu Pvt. Ltd.</p>',
                'template': 'home',
                'status': 'active',
                'order': 0
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created page: {home_page.title}'))
        else:
            self.stdout.write(self.style.WARNING('Home page already exists'))
        
        # Create about page
        about_page, created = Page.objects.get_or_create(
            slug='about',
            defaults={
                'title': 'About Us',
                'content': '<p>Learn more about our company and services.</p>',
                'template': 'default',
                'status': 'active',
                'order': 1
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created page: {about_page.title}'))
        else:
            self.stdout.write(self.style.WARNING('About page already exists'))
        
        self.stdout.write(self.style.SUCCESS('Site setup complete!'))

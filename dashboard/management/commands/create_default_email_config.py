from django.core.management.base import BaseCommand
from dashboard.models import EmailConfiguration


class Command(BaseCommand):
    help = 'Create default email configuration if none exists'

    def handle(self, *args, **options):
        # Check if any email configuration exists
        if EmailConfiguration.objects.exists():
            self.stdout.write(
                self.style.WARNING('Email configuration already exists. Skipping creation.')
            )
            return

        # Create default configuration
        config = EmailConfiguration.objects.create(
            name='Default Email Configuration',
            is_active=True,
            backend='console',
            email_host='smtp.gmail.com',
            email_port=587,
            email_use_tls=True,
            email_host_user='',
            email_host_password='',
            from_email='noreply@localhost',
            from_name='Himwatkhanda Vastu',
            admin_email='admin@localhost',
            notes='Default console email configuration for development. Update this for production.'
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created default email configuration: {config.name}')
        )
        self.stdout.write(
            self.style.WARNING('Remember to update this configuration with your SMTP settings for production!')
        )

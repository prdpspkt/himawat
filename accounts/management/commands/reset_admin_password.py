from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Reset admin user password to admin123'

    def handle(self, *args, **options):
        # Find admin user (is_staff=True and is_superuser=True)
        try:
            admin_user = User.objects.filter(is_staff=True, is_superuser=True).first()

            if admin_user:
                # Reset password
                admin_user.set_password('admin123')
                admin_user.save()

                self.stdout.write(
                    self.style.SUCCESS(f'Successfully reset password for user: {admin_user.username}')
                )
                self.stdout.write(
                    self.style.WARNING(f'Username: {admin_user.username}')
                )
                self.stdout.write(
                    self.style.WARNING(f'New Password: admin123')
                )
                self.stdout.write(
                    self.style.WARNING('Please change this password immediately after logging in!')
                )
            else:
                # No admin user found, create one
                admin_user = User.objects.create_superuser(
                    username='admin',
                    email='admin@himawatkhandavastu.com',
                    password='admin123',
                    role='admin',
                    status='active'
                )

                self.stdout.write(
                    self.style.SUCCESS('Created new admin user')
                )
                self.stdout.write(
                    self.style.WARNING(f'Username: {admin_user.username}')
                )
                self.stdout.write(
                    self.style.WARNING(f'Password: admin123')
                )
                self.stdout.write(
                    self.style.WARNING('Please change this password immediately after logging in!')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )

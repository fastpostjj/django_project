from django.core.management import BaseCommand

from user_auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.pro',
            first_name='Admin',
            last_name='SuperAdmin',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('123abc123')
        user.save()
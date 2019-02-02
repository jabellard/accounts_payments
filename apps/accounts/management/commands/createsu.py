from django.core.management.base import BaseCommand
from apps.accounts.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='admin')
            print(user)
        except User.DoesNotExist:
            User.objects.create_superuser('admin', 'admin@localhost.com', 'admin')

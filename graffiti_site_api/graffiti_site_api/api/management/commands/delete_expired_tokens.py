from django.core.management.base import BaseCommand
from ...models import ActivationToken


class Command(BaseCommand):
    help = "Deletes all expired tokens from the database"
    
    def handle(self, *args, **options):
        n = ActivationToken.objects.delete_expired()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {n} token(s)')
        )

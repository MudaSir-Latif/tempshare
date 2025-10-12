# core/management/commands/cleanup_expired.py
from django.core.management.base import BaseCommand
from core.models import FileShare, URLShare
from django.utils import timezone


class Command(BaseCommand):
    help = "Delete expired FileShare and URLShare entries (and delete files)."

    def handle(self, *args, **options):
        now = timezone.now()
        expired_files = FileShare.objects.filter(expires_at__lte=now)
        expired_urls = URLShare.objects.filter(expires_at__lte=now)

        total = expired_files.count() + expired_urls.count()
        self.stdout.write(f"Found {total} expired items.")

        for f in expired_files:
            try:
                f.delete()
                self.stdout.write(f"Deleted file share {f.token}")
            except Exception as e:
                self.stdout.write(f"Error deleting file {f.token}: {e}")

        for u in expired_urls:
            try:
                token = u.token
                u.delete()
                self.stdout.write(f"Deleted url share {token}")
            except Exception as e:
                self.stdout.write(f"Error deleting url {token}: {e}")

        self.stdout.write("Cleanup completed.")

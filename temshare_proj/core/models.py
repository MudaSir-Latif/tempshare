# core/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
import secrets


def get_burnout_time(minutes=5):
    """Returns a timestamp minutes from now (for expiry)."""
    return timezone.now() + timedelta(minutes=minutes)


def generate_token(n=8):
    """Generates a short unique token."""
    return secrets.token_urlsafe(n)[:n]


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class FileShare(TimestampedModel):
    token = models.CharField(max_length=16, unique=True, default=generate_token)
    file = models.FileField(upload_to="uploads/")
    expires_at = models.DateTimeField(default=get_burnout_time)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def delete(self, using=None, keep_parents=False):
        # delete file from disk before removing model entry
        try:
            storage = self.file.storage
            name = self.file.name
            if storage.exists(name):
                storage.delete(name)
        except Exception:
            pass
        super().delete(using=using, keep_parents=keep_parents)

    def __str__(self):
        return f"FileShare({self.token})"


class URLShare(TimestampedModel):
    token = models.CharField(max_length=16, unique=True, default=generate_token)
    original_url = models.URLField()
    expires_at = models.DateTimeField(default=get_burnout_time)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"URLShare({self.token})"

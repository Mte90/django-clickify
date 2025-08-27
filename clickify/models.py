from django.db import models
import uuid


class DownloadTarget(models.Model):
    """
    Represents a file or asset that can be downloaded.
    This model decouples the asset from its actual URL, allowing the URL to change without loosing the download history
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,
                            help_text="A user-freiendly name for the download target, e.g., Monthly Report PDF"
                            )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="A unique slug for the URL. E.g., 'monthly-report-pdf' "
    )
    target_url = models.URLField(
        max_length=2048,
        help_text="The actual URL to the file (e.g., on S3, Dropbox, etc)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DownloadClick(models.Model):
    """
    Logs a single download event for a DownloadTarget.
    """
    target = models.ForeignKey(
        DownloadTarget,
        on_delete=models.CASCADE,
        related_name='clicks'
    )
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Click on {self.target.name} at {self.timestamp}"

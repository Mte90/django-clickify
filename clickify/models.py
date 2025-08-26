from django.db import models


class DownloadClick(models.Model):
    file_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} clicked from {self.ip_address}"

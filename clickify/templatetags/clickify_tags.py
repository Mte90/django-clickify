from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def track_url(slug):
    """
    A template tag that returns the tracked URL for a DownloadTarget slug
    Usage: {% track_url 'my-download-slug' %}
    """

    return reverse('clickify:track_download', kwargs={'slug': slug})

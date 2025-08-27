from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.conf import settings
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.decorators import ratelimit
from .models import DownloadTarget
from .utils import create_download_click


@ratelimit(key='ip', rate=lambda r, g: getattr(settings, 'CLICKIFY_RATE_LIMIT', '5/m'), block=True)
def track_download(request, slug):
    """track download
    Track download click for a DownloadTarget and then redirects its actual file URL
    """

    try:
        target = get_object_or_404(DownloadTarget, slug=slug)
        # Call the helper function to do the actual tracking
        create_download_click(target=target, request=request)
        return HttpResponseRedirect(target.target_url)
    except Ratelimited:
        return HttpResponseForbidden("Rate limit exceeded. Please try again later.")

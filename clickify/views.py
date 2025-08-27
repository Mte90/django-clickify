from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from ipware import get_client_ip
from .models import DownloadTarget, DownloadClick
from .utils import get_geolocation


def track_download(request, slug):
    """track download

    Track download click for a DownloadTarget and then redirects its actual file URL
    """

    target = get_object_or_404(DownloadTarget, slug=slug)
    rate = getattr(settings, 'CLICKIFY_RATE_LIMIT', '5/m')

    @ratelimit(key='ip', rate=rate, block=True)
    def inner(request):
        ip, is_routable = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        country, city = get_geolocation(ip)

        DownloadClick.objects.create(
            target=target,
            ip_address=ip,
            user_agent=user_agent,
            country=country,
            city=city
        )

        return HttpResponseRedirect(target.target_url)
    return inner(request)

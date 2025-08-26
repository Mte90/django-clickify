from .utils import get_geolocation
from ipware import get_client_ip
from django.http import FileResponse, Http404
from django.conf import settings
from .models import DownloadClick
from django_ratelimit.decorators import ratelimit
import os

rate = getattr(settings, 'CLICKIFY_RATE_LIMIT', '5/m')


@ratelimit(key='ip', rate=rate, block=True)
def track_download(request, file_path):
    ip, is_routable = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")

    # GeoIP
    country, city = get_geolocation(ip)

    # Saveto DB
    DownloadClick.objects.create(
        file_name=os.path.basename(file_path),
        ip_address=ip,
        user_agent=user_agent,
        country=country,
        city=city
    )

    # Serve the file
    # Securely build the absolute path to prevent path traversal vulnerability
    absolute_path = os.path.abspath(
        os.path.join(settings.MEDIA_ROOT, file_path))
    media_root_abs = os.path.abspath(settings.MEDIA_ROOT)

    # Check for path traversal
    if not absolute_path.startswith(media_root_abs):
        raise Http404("File not found")

    if not os.path.exists(absolute_path):
        raise Http404("File not found")

    try:
        fh = open(absolute_path, 'rb')
        response = FileResponse(fh, as_attachment=True)
        return response
    except FileNotFoundError:
        raise Http404("File not found")

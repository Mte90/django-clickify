from ipware import get_client_ip
from django.http import FileResponse, Http404
from django.conf import settings
from .models import DownloadClick
from django_ratelimit.decorators import ratelimit
import geoip2.database
import os


@ratelimit(key='ip', rate='5/m', block=True)
def track_download(request, file_path):
    ip, is_routable = get_client_ip(request)
    user_agent = request.META.get("HTTP_USER_AGENT", "")
    country = city = ""

    # GeoIP
    try:
        reader = geoip2.database.Reader(settings.GEOIP_PATH)
        response = reader.city(ip)
        country = response.country.name
        city = response.city.name
    except Exception:
        pass

    # Saveto DB
    DownloadClick.objects.create(
        file_name=os.path.basename(file_path),
        ip_address=ip,
        user_agent=user_agent,
        country=country,
        city=city
    )

    # Serve the file
    absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if not os.path.exists(absolute_path):
        raise Http404("File not found")

    return FileResponse(open(absolute_path, 'rb'), as_attachment=True)

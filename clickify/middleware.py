from django.conf import settings
from django.core.exceptions import PermissionDenied
from ipware import get_client_ip


class IPFilterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_allowlist = getattr(settings, 'CLICKIFY_IP_ALLOWLIST', [])
        self.ip_blocklist = getattr(settings, 'CLICKIFY_IP_BLOCKLIST', [])

    def __call__(self, request):
        client_ip, _ = get_client_ip(request)

        if self.ip_allowlist and client_ip not in self.ip_allowlist:
            raise PermissionDenied("IP address not allowed.")

        if client_ip in self.ip_blocklist:
            raise PermissionDenied("IP address blocked.")

        response = self.get_response(request)
        return response

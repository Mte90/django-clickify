from django.test import TestCase, RequestFactory
from django.core.exceptions import PermissionDenied
from clickify.middleware import IPFilterMiddleware
from django.conf import settings
import django

# Configure Django settings for the test environment
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            },
        },
        INSTALLED_APPS=[
            'clickify'
        ]
    )
    django.setup()


class IPFilterMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = lambda request: None

    def test_ip_allowed(self):
        middleware = IPFilterMiddleware(self.get_response)
        request = self.factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '127.0.0.1'

        with self.settings(CLICKIFY_IP_ALLOWLIST=['127.0.0.1']):
            response = middleware(request)
            self.assertIsNone(response)

    def test_ip_not_in_allowlist(self):
        middleware = IPFilterMiddleware(self.get_response)
        request = self.factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '10.0.0.1'

        with self.settings(CLICKIFY_IP_ALLOWLIST=['127.0.0.1']):
            with self.assertRaises(PermissionDenied):
                middleware(request)

    def test_ip_in_blocklist(self):
        middleware = IPFilterMiddleware(self.get_response)
        request = self.factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '10.0.0.1'

        with self.settings(CLICKIFY_IP_BLOCKLIST=['10.0.0.1']):
            with self.assertRaises(PermissionDenied):
                middleware(request)

import os
from django.core.cache import cache
from django.test import TestCase, RequestFactory, override_settings
from django.core.exceptions import PermissionDenied
from clickify.middleware import IPFilterMiddleware
from django.conf import settings
from django.http import Http404
from clickify.views import track_download
from clickify.models import DownloadClick
from unittest.mock import patch
from django_ratelimit.exceptions import Ratelimited
from django.urls import reverse


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


@patch('clickify.views.get_geolocation', return_value=('Test Country', 'Test City'))
class TrackDownloadViewTest(TestCase):
    def setUp(self):
        cache.clear()
        self.factory = RequestFactory()
        # Create a dummy file for testing
        self.file_path = os.path.join(settings.MEDIA_ROOT, 'test_file.txt')

        # Ensures media root exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        with open(self.file_path, 'w') as f:
            f.write('test content')

    def tearDown(self):
        # Clean up the dummy file
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_download_creates_click(self, mock_get_geolocation):
        self.assertEqual(DownloadClick.objects.count(), 0)

        url = reverse('track_download', kwargs={'file_path': 'test_file.txt'})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(DownloadClick.objects.count(), 1)
        click = DownloadClick.objects.first()
        self.assertEqual(click.file_name, 'test_file.txt')

    def test_download_nonexistent_file(self, mock_get_geolocation):
        url = reverse('track_download', kwargs={
                      'file_path': 'nonexistent.txt'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    

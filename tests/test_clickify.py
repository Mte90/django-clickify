import os
import tempfile
from django.test import TestCase, RequestFactory, override_settings
from django.core.exceptions import PermissionDenied
from clickify.middleware import IPFilterMiddleware
from django.conf import settings
from django.http import Http404
from clickify.views import track_download
from clickify.models import DownloadClick
from unittest.mock import patch


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
        request = self.factory.get('/download/test_file.txt')

        response = track_download(request, 'test_file.txt')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(DownloadClick.objects.count(), 1)
        click = DownloadClick.objects.first()
        self.assertEqual(click.file_name, 'test_file.txt')

    def test_download_nonexistent_file(self, mock_get_geolocation):
        request = self.factory.get('/download/nonexistent.txt')

        with self.assertRaises(Http404):
            track_download(request, 'nonexistent.txt')

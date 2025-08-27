from django.template import Template, Context
import os
from django.core.cache import cache
from django.test import TestCase, RequestFactory, override_settings
from django.core.exceptions import PermissionDenied
from clickify.middleware import IPFilterMiddleware
from django.conf import settings
from django.http import Http404
from clickify.views import track_download
from clickify.models import DownloadClick, DownloadTarget
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
        self.target = DownloadTarget.objects.create(
            name="Test File",
            slug='test-file',
            target_url="https://example.com/test-file.zip"
        )

    def test_download_creates_click_and_redirects(self, mock_get_geolocation):
        self.assertEqual(self.target.clicks.count(), 0)

        url = reverse('clickify:track_download',
                      kwargs={'slug': self.target.slug})
        response = self.client.get(url)

        # Check for successfull redirects
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.target.target_url)

        # Check that the clicks was recorded and associated with the correct target
        self.assertEqual(self.target.clicks.count(), 1)
        click = self.target.clicks.first()
        # Check the mock data is saved or not
        self.assertEqual(click.country, 'Test Country')

    def test_download_nonexistent_file(self, mock_get_geolocation):
        url = reverse('clickify:track_download', kwargs={
                      'slug': 'nonexistent-slug'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @override_settings(CLICKIFY_RATE_LIMIT='1/m',)
    def test_rate_limit_exceeded(self, mock_get_geolocation):
        url = reverse('clickify:track_download',
                      kwargs={'slug': self.target.slug})

        # First request should succeed
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Second request should blocked with 403 status code
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class ClickifyTemplateTagTest(TestCase):
    def setUp(self):
        self.target = DownloadTarget.objects.create(
            name="Test File",
            slug="test-file",
            target_url="https://example.com/test-file.zip"
        )

    def test_track_url_tag(self):
        # The template content we want to render
        template_to_render = """
            {% load clickify_tags %}
            {% track_url 'test-file' %}
        """

        # Create a template object
        t = Template(template_to_render)

        # Render the template
        rendered = t.render(Context({}))

        # The expected URL
        expected_url = reverse('clickify:track_download',
                               kwargs={'slug': 'test-file'})

        # Check that the rendered output is the correct url
        self.assertEqual(rendered.strip(), expected_url)

from unittest.mock import Mock, patch

from django.test import TestCase, override_settings

from clickify.models import ClickLog, TrackedLink
from clickify.utils import create_click_log, get_client_ip, get_geolocation


class CreateClickLogTest(TestCase):
    def setUp(self):
        self.target = TrackedLink.objects.create(
            name="Test Target", slug="test-target", target_url="https://example.com"
        )
        # Create a mock request object
        self.mock_request = Mock()
        self.mock_request.META = {"HTTP_USER_AGENT": "Test Agent"}

    @patch("clickify.utils.get_geolocation")
    @patch("clickify.utils.get_client_ip")
    def test_creates_click_for_routable_ip(
        self, mock_get_client_ip, mock_get_geolocation
    ):
        """
        If the IP is routable, geolocation should be fetched and saved.
        """
        # Configure mocks
        mock_get_client_ip.return_value = ("8.8.8.8", True)  # Routable IP
        mock_get_geolocation.return_value = ("Test Country", "Test City")

        # Call the function
        create_click_log(self.target, self.mock_request)

        # Assertions
        self.assertEqual(ClickLog.objects.count(), 1)
        mock_get_client_ip.assert_called_once_with(self.mock_request)
        mock_get_geolocation.assert_called_once_with("8.8.8.8")

        click = ClickLog.objects.first()
        self.assertEqual(click.ip_address, "8.8.8.8")
        self.assertEqual(click.country, "Test Country")
        self.assertEqual(click.city, "Test City")
        self.assertEqual(click.user_agent, "Test Agent")

    @patch("clickify.utils.get_geolocation")
    @patch("clickify.utils.get_client_ip")
    def test_creates_click_for_non_routable_ip(
        self, mock_get_client_ip, mock_get_geolocation
    ):
        """
        If the IP is not routable, geolocation should be skipped.
        """
        # Configure mocks
        mock_get_client_ip.return_value = ("127.0.0.1", False)  # Non-routable IP

        # Call the function
        create_click_log(self.target, self.mock_request)

        # Assertions
        self.assertEqual(ClickLog.objects.count(), 1)
        mock_get_client_ip.assert_called_once_with(self.mock_request)
        mock_get_geolocation.assert_not_called()  # Ensure this was skipped

        click = ClickLog.objects.first()
        self.assertEqual(click.ip_address, "127.0.0.1")
        self.assertIsNone(click.country)
        self.assertIsNone(click.city)


class GetClientIPTest(TestCase):
    def test_get_client_ip_direct(self):
        request = Mock()
        request.META = {"REMOTE_ADDR": "1.2.3.4"}
        ip, routable = get_client_ip(request)
        self.assertEqual(ip, "1.2.3.4")
        self.assertTrue(routable)

    def test_get_client_ip_x_forwarded_for(self):
        request = Mock()
        request.META = {"HTTP_X_FORWARDED_FOR": "5.6.7.8, 9.10.11.12"}
        ip, routable = get_client_ip(request)
        self.assertEqual(ip, "5.6.7.8")
        self.assertTrue(routable)

    def test_get_client_ip_private(self):
        request = Mock()
        request.META = {"REMOTE_ADDR": "192.168.1.1"}
        ip, routable = get_client_ip(request)
        self.assertEqual(ip, "192.168.1.1")
        self.assertFalse(routable)


class GetGeolocationTest(TestCase):
    @patch("clickify.utils.get_geoip")
    def test_get_geolocation_success(self, mock_get_geoip):
        mock_get_geoip.return_value = {
            "status": "success",
            "country": "Testland",
            "city": "Testville",
        }
        country, city = get_geolocation("1.2.3.4")
        self.assertEqual(country, "Testland")
        self.assertEqual(city, "Testville")

    @patch("clickify.utils.get_geoip")
    def test_get_geolocation_failure(self, mock_get_geoip):
        mock_get_geoip.return_value = {"status": "fail"}
        country, city = get_geolocation("1.2.3.4")
        self.assertIsNone(country)
        self.assertIsNone(city)

    @override_settings(CLICKIFY_GEOLOCATION=False)
    def test_get_geolocation_disabled(self):
        country, city = get_geolocation("1.2.3.4")
        self.assertIsNone(country)
        self.assertIsNone(city)

from django.test import TestCase
from unittest.mock import patch, Mock
from clickify.models import TrackedLink, ClickLog
from clickify.utils import create_click_log


class CreateClickLogTest(TestCase):

    def setUp(self):
        self.target = TrackedLink.objects.create(
            name="Test Target",
            slug="test-target",
            target_url="https://example.com"
        )
        # Create a mock request object
        self.mock_request = Mock()
        self.mock_request.META = {"HTTP_USER_AGENT": "Test Agent"}

    @patch('clickify.utils.get_geolocation')
    @patch('clickify.utils.get_client_ip')
    def test_creates_click_for_routable_ip(self, mock_get_client_ip, mock_get_geolocation):
        """
        If the IP is routable, geolocation should be fetched and saved.
        """
        # Configure mocks
        mock_get_client_ip.return_value = ('8.8.8.8', True)  # Routable IP
        mock_get_geolocation.return_value = ('Test Country', 'Test City')

        # Call the function
        create_click_log(self.target, self.mock_request)

        # Assertions
        self.assertEqual(ClickLog.objects.count(), 1)
        mock_get_client_ip.assert_called_once_with(self.mock_request)
        mock_get_geolocation.assert_called_once_with('8.8.8.8')

        click = ClickLog.objects.first()
        self.assertEqual(click.ip_address, '8.8.8.8')
        self.assertEqual(click.country, 'Test Country')
        self.assertEqual(click.city, 'Test City')
        self.assertEqual(click.user_agent, "Test Agent")

    @patch('clickify.utils.get_geolocation')
    @patch('clickify.utils.get_client_ip')
    def test_creates_click_for_non_routable_ip(self, mock_get_client_ip, mock_get_geolocation):
        """
        If the IP is not routable, geolocation should be skipped.
        """
        # Configure mocks
        mock_get_client_ip.return_value = (
            '127.0.0.1', False)  # Non-routable IP

        # Call the function
        create_click_log(self.target, self.mock_request)

        # Assertions
        self.assertEqual(ClickLog.objects.count(), 1)
        mock_get_client_ip.assert_called_once_with(self.mock_request)
        mock_get_geolocation.assert_not_called()  # Ensure this was skipped

        click = ClickLog.objects.first()
        self.assertEqual(click.ip_address, '127.0.0.1')
        self.assertIsNone(click.country)
        self.assertIsNone(click.city)

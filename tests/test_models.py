from django.test import TestCase

from clickify.models import TrackedLink


class TrackedLinkModelTest(TestCase):
    def test_str_representation(self):
        """Test that the string representation of the object is its name"""
        target = TrackedLink(name="My Test File")
        self.assertEqual(str(target), "My Test File")

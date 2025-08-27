from django.test import TestCase
from django.template import Template, Context
from django.urls import reverse
from clickify.models import DownloadTarget


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

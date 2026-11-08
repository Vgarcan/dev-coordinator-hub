from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.


class DashboardHomeTests(SimpleTestCase):
    """Keep the initial user-facing route and its truthful status testable."""

    def test_home_page_renders_without_a_database(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django foundation ready')
        self.assertContains(response, 'Not connected to agents')

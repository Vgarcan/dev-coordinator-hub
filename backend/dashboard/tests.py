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
        self.assertTemplateUsed(response, 'dashboard/home.html')

    def test_admin_requires_authentication(self):
        """The standard Django admin must not expose its index anonymously."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

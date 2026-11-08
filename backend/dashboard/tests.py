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
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'partials/_feature_tile.html')
        self.assertTemplateUsed(response, 'partials/_site_header.html')
        self.assertTemplateUsed(response, 'partials/_nav_links.html')
        self.assertContains(response, 'class="dc-desktop-nav"')
        self.assertContains(response, 'class="dc-mobile-menu"')
        self.assertContains(response, 'dashboard/css/app.css')
        self.assertContains(response, 'Skip to main content')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, reverse('repositories:list'))

    def test_admin_requires_authentication(self):
        """The standard Django admin must not expose its index anonymously."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

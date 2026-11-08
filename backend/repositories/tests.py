from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Repository

# Create your tests here.


class RepositoryModelTests(TestCase):
    """Validate the local GitHub identifier before the item is saved."""

    def test_default_status_is_candidate(self):
        repository = Repository.objects.create(full_name='example/demo')
        self.assertEqual(repository.tracking_status, Repository.TrackingStatus.CANDIDATE)
        self.assertEqual(str(repository), 'example/demo')
        self.assertEqual(repository.github_url, 'https://github.com/example/demo')

    def test_full_name_requires_owner_and_repository(self):
        repository = Repository(full_name='not-a-full-name')
        with self.assertRaises(ValidationError):
            repository.full_clean()


class RepositoryListTests(TestCase):
    """Only active staff members may view the inventory."""

    @classmethod
    def setUpTestData(cls):
        cls.staff = get_user_model().objects.create_user(
            username='staff', password='test-password', is_staff=True,
        )
        cls.member = get_user_model().objects.create_user(
            username='member', password='test-password',
        )
        cls.url = reverse('repositories:list')

    def test_anonymous_user_is_redirected_to_admin_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_non_staff_member_is_denied(self):
        self.client.force_login(self.member)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_staff_sees_empty_inventory(self):
        self.client.force_login(self.staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'repositories/list.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'partials/_site_header.html')
        self.assertTemplateUsed(response, 'partials/_nav_links.html')
        self.assertContains(response, 'class="dc-desktop-nav"')
        self.assertContains(response, 'class="dc-mobile-menu"')
        self.assertContains(response, 'dashboard/css/app.css')
        self.assertContains(response, 'aria-current="page"')
        self.assertContains(response, 'No repositories registered yet.')

    def test_staff_sees_registered_repositories(self):
        Repository.objects.create(
            full_name='example/sample',
            description='Test repository',
            tracking_status=Repository.TrackingStatus.TRACKED,
        )
        self.client.force_login(self.staff)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'repositories/_repository_card.html')
        self.assertContains(response, 'example/sample')
        self.assertContains(response, 'Test repository')
        self.assertContains(response, 'https://github.com/example/sample')
        self.assertContains(response, 'Tracked')
        self.assertContains(response, 'Inventory only')

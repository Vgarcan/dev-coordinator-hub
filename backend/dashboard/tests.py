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
        self.assertContains(response, reverse('dashboard:tasks'))
        self.assertContains(response, reverse('dashboard:agents'))

    def test_admin_requires_authentication(self):
        """The standard Django admin must not expose its index anonymously."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

class DashboardTaskDemoTests(SimpleTestCase):
    """Keep fictional task browsing separate from operational coordination."""

    def test_demo_page_uses_shared_templates(self):
        response = self.client.get(reverse('dashboard:tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/tasks.html')
        self.assertTemplateUsed(response, 'dashboard/_task_card.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertContains(response, 'Simulation only')
        self.assertContains(response, 'No agents are connected')
        self.assertContains(response, 'DEMO-001')
        self.assertEqual(len(response.context['tasks']), 4)

    def test_status_filter_is_read_only(self):
        response = self.client.get(reverse('dashboard:tasks'), {'status': 'review'})
        self.assertEqual([item['id'] for item in response.context['tasks']], ['DEMO-003'])
        self.assertContains(response, 'DEMO-003')
        self.assertNotContains(response, 'DEMO-001')

    def test_unknown_status_does_not_change_results(self):
        response = self.client.get(reverse('dashboard:tasks'), {'status': 'untrusted'})
        self.assertFalse(response.context['is_filtered'])
        self.assertEqual(len(response.context['tasks']), 4)

    def test_no_mock_records_for_a_valid_status(self):
        response = self.client.get(reverse('dashboard:tasks'), {'status': 'running'})
        self.assertEqual(response.context['tasks'], [])
        self.assertContains(response, 'No example tasks in this state')

    def test_mock_page_has_no_write_controls(self):
        response = self.client.get(reverse('dashboard:tasks'))
        self.assertNotContains(response, 'method="post"')
        self.assertNotContains(response, 'Run agent')
        self.assertNotContains(response, 'Approve task')

class DotenvConfigurationTests(SimpleTestCase):
    """Local .env is optional and never overwrites process configuration."""

    def test_existing_os_environment_value_takes_precedence(self):
        import os
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        from dotenv import load_dotenv

        with tempfile.TemporaryDirectory() as directory:
            sample = Path(directory) / '.env'
            sample.write_text('DCH_TEST_SETTING=from_file\n', encoding='utf-8')
            with patch.dict(os.environ, {'DCH_TEST_SETTING': 'from_process'}):
                load_dotenv(dotenv_path=sample, override=False)
                self.assertEqual(os.environ['DCH_TEST_SETTING'], 'from_process')

    def test_missing_dotenv_is_optional(self):
        import tempfile
        from pathlib import Path

        from dotenv import load_dotenv

        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / 'missing.env'
            self.assertFalse(load_dotenv(dotenv_path=missing, override=False))

class DashboardAgentGalleryTests(SimpleTestCase):
    """A public-safe role preview is never mistaken for live agent inventory."""

    def test_gallery_renders_three_fictional_profiles(self):
        response = self.client.get(reverse('dashboard:agents'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/agents.html')
        self.assertTemplateUsed(response, 'dashboard/_agent_card.html')
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'partials/_nav_links.html')
        self.assertEqual(
            [agent['key'] for agent in response.context['agents']],
            ['codex', 'claude', 'ollama'],
        )
        self.assertContains(response, 'Codex CLI')
        self.assertContains(response, 'Claude Code')
        self.assertContains(response, 'Ollama')
        self.assertContains(response, 'Concept only')
        self.assertContains(response, 'Not connected')

    def test_gallery_has_no_agent_controls_or_backend_probes(self):
        response = self.client.get(reverse('dashboard:agents'))
        self.assertNotContains(response, 'method="post"')
        self.assertNotContains(response, 'Run agent')
        self.assertNotContains(response, 'Connect agent')
        self.assertNotContains(response, 'Approve task')
        self.assertContains(response, 'No authentication, model availability,')

    def test_navigation_marks_only_agents_active(self):
        response = self.client.get(reverse('dashboard:agents'))
        rendered = response.content.decode('utf-8')
        # Template whitespace between attributes is intentional.
        self.assertRegex(rendered, r'href="/agents/"\s+aria-current="page"')
        self.assertNotRegex(rendered, r'href="/"\s+aria-current="page"')

    def test_overview_links_to_gallery(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertContains(response, reverse('dashboard:agents'))

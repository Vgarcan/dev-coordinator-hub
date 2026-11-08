"""Static frontend contracts runnable without installing Django.

These tests do not replace Django's template rendering, browser inspection,
or accessibility audits. They prevent known source-level regressions.
"""

from pathlib import Path
import re
import unittest


# Derive paths from this file so the tests work from any current directory.
BACKEND = Path(__file__).resolve().parents[1]
TEMPLATES = BACKEND / "dashboard" / "templates" / "dashboard"
SHARED = BACKEND / "templates"
STYLES = BACKEND / "dashboard" / "static" / "dashboard" / "css"


def source(path):
    """Read one project file without importing Django or hitting the network."""
    return path.read_text(encoding="utf-8")


class FrontendSourceContractTests(unittest.TestCase):
    """Guard the three-page mock UI against avoidable regressions."""

    def test_three_pages_extend_the_one_base_template(self):
        for page in ("home.html", "tasks.html", "agents.html"):
            with self.subTest(page=page):
                markup = source(TEMPLATES / page)
                self.assertIn("{% extends 'base.html' %}", markup)
                self.assertIn("<h1", markup)

    def test_shared_header_has_distinct_mobile_and_desktop_navigation(self):
        header = source(SHARED / "partials" / "_site_header.html")
        self.assertIn('class="dc-desktop-nav"', header)
        self.assertIn('class="dc-mobile-menu"', header)
        self.assertEqual(header.count("{% include 'partials/_nav_links.html' %}"), 2)

    def test_closed_mobile_details_stays_hidden(self):
        # Chromium reproduction: .dc-mobile-nav { display:grid } makes
        # a closed <details> child visible unless explicitly hidden.
        css = source(STYLES / "app.css")
        self.assertRegex(
            css,
            r"\.dc-mobile-menu:not\(\[open\]\)\s*>\s*\.dc-mobile-nav\s*"
            r"\{\s*display:\s*none\s*;",
        )
        self.assertIn(".dc-mobile-nav {\n    display: grid;", css)

    def test_desktop_navigation_waits_until_wide_layout(self):
        css = source(STYLES / "app.css")
        self.assertRegex(
            css, r"@media\s*\(min-width:\s*1200px\)\s*\{"
            r"[^}]*\.dc-header-layout[^}]*\}"
            r"\s*\.dc-desktop-nav\s*\{\s*display:\s*flex",
        )
        self.assertNotRegex(
            css, r"@media\s*\(min-width:\s*768px\)\s*\{"
            r"\s*\.dc-header-layout",
        )

    def test_overview_primary_action_is_accessible_without_staff_login(self):
        home = source(TEMPLATES / "home.html")
        self.assertIn(
            '<a class="dc-button dc-button-primary" '
            'href="{% url \'dashboard:tasks\' %}">',
            home,
        )

    def test_demo_pages_have_no_mutation_forms(self):
        tasks = source(TEMPLATES / "tasks.html")
        agents = source(TEMPLATES / "agents.html")
        self.assertIn('method="get"', tasks)
        for markup in (tasks, agents):
            self.assertNotIn('method="post"', markup)
            self.assertNotIn("<script", markup)

    def test_untrusted_agent_details_remain_fictional(self):
        agents = source(TEMPLATES / "agents.html")
        self.assertIn("Concept only", agents)
        self.assertIn("No agents are connected", agents)
        self.assertIn("dashboard/_agent_card.html", agents)


if __name__ == "__main__":
    unittest.main()

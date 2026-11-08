"""Standard-library tests for the non-executing environment preflight."""

import json
import unittest
from unittest.mock import patch

from scripts import preflight


class PreflightTests(unittest.TestCase):
    """Prove inspection reports facts, not operational authorisation."""

    def test_unavailable_tools_never_appear_ready(self):
        report = preflight.inspect_environment(
            which=lambda _name: None,
            django_available=False,
            python_version=(3, 13),
        )
        self.assertEqual(report['cli_on_path'], {
            'git': False, 'codex': False, 'claude': False,
        })
        self.assertFalse(report['safe_for_execution'])
        self.assertEqual(report['subscription_usage'], 'unknown')
        self.assertTrue(report['python']['recommended_3_13'])

    def test_detected_cli_does_not_imply_authentication(self):
        report = preflight.inspect_environment(
            which=lambda name: '/some/path' if name in ('git', 'claude') else None,
            django_available=True,
            python_version=(3, 12),
        )
        self.assertTrue(report['cli_on_path']['claude'])
        self.assertFalse(report['cli_on_path']['codex'])
        self.assertEqual(report['cli_authenticated'], 'not_checked')
        self.assertEqual(report['provider_permission'], 'not_checked')
        self.assertFalse(report['safe_for_execution'])
        self.assertFalse(report['python']['recommended_3_13'])
        self.assertNotIn('/some/path', preflight.report_text(report))

    def test_json_is_valid_and_has_no_credentials(self):
        report = preflight.inspect_environment(
            which=lambda _name: None, django_available=False,
            python_version=(3, 13),
        )
        raw = json.dumps(report)
        self.assertEqual(json.loads(raw)['schema_version'], 1)
        self.assertNotIn('SECRET_KEY', raw)

    def test_cli_detection_never_runs_subprocess(self):
        with patch.object(preflight.shutil, 'which', return_value=None), \
             patch.object(preflight.importlib.util, 'find_spec', return_value=None), \
             patch('subprocess.run', side_effect=AssertionError('command executed')):
            report = preflight.inspect_environment()
            self.assertFalse(report['django_installed'])
            self.assertFalse(report['safe_for_execution'])


if __name__ == '__main__':
    unittest.main()

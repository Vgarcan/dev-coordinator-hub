"""Unit tests for interpreter selection and staged setup, without installs."""

import io
from contextlib import redirect_stdout
import subprocess
import unittest
from unittest.mock import patch

from scripts import setup_local


class InterpreterSelectionTests(unittest.TestCase):
    def setUp(self):
        self.py312 = setup_local.PythonChoice('/opt/python3.12', (3, 12, 11))
        self.py313 = setup_local.PythonChoice('/opt/python3.13', (3, 13, 5))
        self.old = setup_local.PythonChoice('/opt/python3.9', (3, 9, 21))

    def test_choose_among_multiple_valid_versions(self):
        with redirect_stdout(io.StringIO()):
            chosen = setup_local.select_python(
                [self.py313, self.py312, self.old], interactive=True,
                reader=lambda prompt: '2',
            )
        self.assertEqual(chosen, self.py312)

    def test_reject_unsupported_then_retry(self):
        answers = iter(['3', '1'])
        with redirect_stdout(io.StringIO()):
            chosen = setup_local.select_python(
                [self.py313, self.py312, self.old], interactive=True,
                reader=lambda prompt: next(answers),
            )
        self.assertEqual(chosen, self.py313)

    def test_noninteractive_requires_explicit_choice(self):
        with self.assertRaisesRegex(ValueError, '--python'):
            with redirect_stdout(io.StringIO()):
                setup_local.select_python(
                    [self.py312, self.py313], interactive=False,
                )

    def test_single_compatible_version_selected_without_prompt(self):
        with redirect_stdout(io.StringIO()):
            chosen = setup_local.select_python(
                [self.old, self.py312], interactive=False,
            )
        self.assertEqual(chosen, self.py312)

    def test_explicit_path_is_probed_and_validated(self):
        with patch.object(setup_local, 'probe_python', return_value=self.py313):
            self.assertEqual(
                setup_local.select_python([], requested='/opt/python3.13'),
                self.py313,
            )
        with patch.object(setup_local, 'probe_python', return_value=self.old):
            with self.assertRaisesRegex(ValueError, 'unsupported'):
                setup_local.select_python([], requested='/opt/python3.9')

    def test_discovery_deduplicates_aliases(self):
        with patch.object(
            setup_local, 'candidate_executables',
            return_value=['python3', '/opt/python3.13', '/opt/python3.12'],
        ), patch.object(
            setup_local, 'probe_python',
            side_effect=[self.py313, self.py313, self.py312],
        ):
            results = setup_local.discover_pythons()
        self.assertEqual(results, [self.py313, self.py312])

    def test_unrecognised_probe_returns_none(self):
        with patch.object(
            setup_local.subprocess, 'run',
            return_value=subprocess.CompletedProcess(['python'], 1, '', ''),
        ):
            self.assertIsNone(setup_local.probe_python('bad-python'))

    def test_failed_stage_reports_false(self):
        with patch.object(
            setup_local.subprocess, 'run',
            return_value=subprocess.CompletedProcess(['python'], 4),
        ):
            self.assertFalse(setup_local.run_stage('Sample failure', ['python']))

    def test_python_version_314_supported_by_current_django(self):
        self.assertTrue(
            setup_local.PythonChoice('/opt/python3.14', (3, 14, 0)).supported
        )


if __name__ == '__main__':
    unittest.main()

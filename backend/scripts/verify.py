#!/usr/bin/env python3
"""Validate the vanilla Django foundation without requiring GitHub Actions.

Use "python scripts/verify.py" for standard-library-only checks or add
"--full" when Django is installed to run migrations and the Django test suite.
"""

import argparse
import ast
import importlib.util
import os
from pathlib import Path
import secrets
import subprocess
import sys


# Resolve the backend folder relative to this file, not the terminal's cwd.
BACKEND_DIR = Path(__file__).resolve().parent.parent
REQUIRED_FILES = (
    'manage.py',
    'config/settings.py',
    'config/urls.py',
    'config/asgi.py',
    'config/wsgi.py',
    'dashboard/apps.py',
    'dashboard/views.py',
    'dashboard/tests.py',
    'repositories/models.py',
    'repositories/admin.py',
    'repositories/views.py',
    'repositories/tests.py',
    'repositories/migrations/0001_initial.py',
    'repositories/templates/repositories/list.html',
)
EXCLUDED_FOLDERS = frozenset({'.venv', 'venv', '__pycache__'})


def check_python_sources() -> bool:
    """Parse all source files without importing or modifying Django."""
    failures = []

    for relative_path in REQUIRED_FILES:
        if not (BACKEND_DIR / relative_path).is_file():
            failures.append(f'Missing required project file: {relative_path}')

    source_count = 0
    for path in sorted(BACKEND_DIR.rglob('*.py')):
        if any(folder in EXCLUDED_FOLDERS for folder in path.relative_to(BACKEND_DIR).parts):
            continue
        source_count += 1
        try:
            # Parsing detects syntax problems without generating files or running code.
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        except (SyntaxError, UnicodeError, OSError) as exc:
            failures.append(f'{path.relative_to(BACKEND_DIR)}: {exc}')

    for failure in failures:
        print(f'FAIL: {failure}', file=sys.stderr)

    if failures:
        print(f'STATIC CHECK FAILED: {len(failures)} problem(s)')
        return False

    print(f'STATIC CHECK PASSED: {source_count} Python file(s) parsed; '
          'expected project and app files present.')
    print('NOTE: Syntax validation is not Django runtime or migration validation.')
    return True


def run_django_checks() -> bool:
    """Run actual Django checks on the ignored local development SQLite database."""
    if importlib.util.find_spec('django') is None:
        print('FULL CHECK BLOCKED: Django is not installed in this Python environment.',
              file=sys.stderr)
        print('Install backend/requirements.txt in a virtual environment, then retry.',
              file=sys.stderr)
        return False

    environment = os.environ.copy()
    # The temporary key is used only for this subprocess validation session.
    environment.setdefault('DJANGO_SECRET_KEY', secrets.token_urlsafe(48))
    environment.setdefault('DJANGO_DEBUG', '0')
    environment.setdefault('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')

    commands = (
        ('Django system checks', ('check',)),
        ('Migration drift check', ('makemigrations', '--check', '--dry-run')),
        ('Apply local development migrations', ('migrate', '--noinput')),
        ('Django tests', ('test', '--noinput')),
    )
    for label, args in commands:
        print(f'RUNNING: {label}', flush=True)
        result = subprocess.run(
            [sys.executable, 'manage.py', *args],
            cwd=BACKEND_DIR,
            env=environment,
            check=False,
        )
        if result.returncode:
            print(f'FULL CHECK FAILED: {label} (exit {result.returncode})',
                  file=sys.stderr)
            return False

    print('FULL CHECK PASSED: Django checks, migrations and tests.')
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--full', action='store_true',
        help='Additionally run Django checks, migration drift detection and tests.',
    )
    options = parser.parse_args()

    if not check_python_sources():
        return 1
    if options.full and not run_django_checks():
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

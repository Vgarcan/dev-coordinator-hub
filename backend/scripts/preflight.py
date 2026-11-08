#!/usr/bin/env python3
"""Report local development prerequisites without invoking agents or Django.

This inspection uses the Python standard library only. It never contacts GitHub,
executes another command, reads credentials, or modifies local project files.
"""

import argparse
import importlib.util
import json
import shutil
import sys


SCHEMA_VERSION = 1


def inspect_environment(*, which=None, django_available=None, python_version=None):
    """Describe availability, keeping authentication and licence status unknown.

    Optional inputs support isolated unit tests without relying on host tools.
    """
    which = which if which is not None else shutil.which
    python_version = python_version or sys.version_info[:2]
    if django_available is None:
        django_available = importlib.util.find_spec('django') is not None

    # Checking PATH only establishes whether a command appears to be installed.
    # Never invoke CLIs here: commands may require authentication or spend tokens.
    tools = {
        name: bool(which(name)) for name in ('git', 'codex', 'claude')
    }
    return {
        'schema_version': SCHEMA_VERSION,
        'inspection': 'read_only_local',
        'python': {
            'major': python_version[0],
            'minor': python_version[1],
            'recommended_3_13': tuple(python_version[:2]) == (3, 13),
        },
        'django_installed': bool(django_available),
        'cli_on_path': tools,
        'cli_authenticated': 'not_checked',
        'provider_permission': 'not_checked',
        'subscription_usage': 'unknown',
        'safe_for_execution': False,
    }


def report_text(report):
    """Return an easily readable report without paths or secret values."""
    python = report['python']
    lines = [
        'Dev Coordination Hub — local read-only preflight',
        f"Python: {python['major']}.{python['minor']}",
        f"Python 3.13 recommended match: {python['recommended_3_13']}",
        f"Django import available: {report['django_installed']}",
    ]
    for cli, available in report['cli_on_path'].items():
        lines.append(f'{cli} on PATH: {available}')
    lines.extend([
        'CLI authentication / usage / organisation permissions: NOT CHECKED',
        'No agent command, network request or Django operation was executed.',
        'This report does NOT authorise or prove readiness for agent execution.',
    ])
    return '\n'.join(lines)


def main(argv=None):
    """Print a human-readable or JSON snapshot; do not change any host state."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Output safe JSON.')
    args = parser.parse_args(argv)
    report = inspect_environment()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report_text(report))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

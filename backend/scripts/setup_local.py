#!/usr/bin/env python3
"""Set up and validate a local Django development environment.

Discover installed Python interpreters, let an interactive user choose one,
then install dependencies only into backend/.venv. No sudo, agent execution,
service installation, or public deployment is performed.
"""

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


BACKEND = Path(__file__).resolve().parent.parent
SUPPORTED = {(3, minor) for minor in range(10, 15)}
PREFERRED = (3, 13)
PROBE = (
    'import sys; v=sys.version_info; '
    'print(f"{v.major}.{v.minor}.{v.micro}|{sys.executable}")'
)


@dataclass(frozen=True)
class PythonChoice:
    """An installed, probed executable (not a claimed PATH alias)."""

    executable: str
    version: tuple[int, int, int]

    @property
    def supported(self):
        return self.version[:2] in SUPPORTED

    @property
    def preferred(self):
        return self.version[:2] == PREFERRED


def probe_python(executable):
    """Inspect one interpreter without installing packages or importing Django."""
    try:
        result = subprocess.run(
            [str(executable), '-c', PROBE],
            capture_output=True, text=True, timeout=8, check=False,
        )
        if result.returncode != 0:
            return None
        version_text, actual_exe = result.stdout.strip().split('|', 1)
        version = tuple(int(part) for part in version_text.split('.'))
        if len(version) != 3 or not actual_exe:
            return None
        return PythonChoice(actual_exe, version)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


def candidate_executables():
    """Find interpreters in PATH and, on Windows, via the Python launcher.

    This intentionally does not search the whole filesystem: use --python for
    an interpreter installed somewhere outside these conventional locations.
    """
    candidates = [getattr(sys, '_base_executable', sys.executable)]
    for name in ('python', 'python3', *(
        f'python3.{minor}' for minor in range(10, 15)
    )):
        match = shutil.which(name)
        if match:
            candidates.append(match)

    if os.name == 'nt':
        launcher = shutil.which('py')
        if launcher:
            try:
                result = subprocess.run(
                    [launcher, '-0p'], capture_output=True,
                    text=True, timeout=8, check=False,
                )
                if result.returncode == 0:
                    for line in result.stdout.splitlines():
                        match = re.search(
                            r'([A-Za-z]:\\.+?\\python(?:\d+)?\.exe)\s*$',
                            line, re.IGNORECASE,
                        )
                        if match:
                            candidates.append(match.group(1))
            except (OSError, subprocess.TimeoutExpired):
                pass
    return candidates


def discover_pythons():
    """Deduplicate aliases, retaining distinct physical Python installations."""
    found = {}
    for executable in candidate_executables():
        info = probe_python(executable)
        if info:
            key = os.path.normcase(os.path.realpath(info.executable))
            found[key] = info
    return sorted(
        found.values(),
        key=lambda item: (
            not item.supported,
            not item.preferred,
            tuple(-part for part in item.version),
            item.executable,
        ),
    )


def display_pythons(options):
    """Make version, path and Django compatibility explicit to the user."""
    print('Python interpreters detected:')
    for index, option in enumerate(options, 1):
        version = '.'.join(map(str, option.version))
        label = 'recommended' if option.preferred else (
            'supported' if option.supported else 'unsupported'
        )
        print(f'  {index}. Python {version} [{label}] — {option.executable}')


def select_python(options, *, requested=None, interactive=None, reader=input):
    """Select an explicitly requested executable or ask when there is a choice."""
    if requested:
        resolved = shutil.which(requested) or requested
        selected = probe_python(resolved)
        if not selected:
            raise ValueError(f'Cannot execute Python: {requested}')
        if not selected.supported:
            raise ValueError('Selected Python is unsupported by Django 5.2 (use 3.10–3.14).')
        return selected

    compatible = [option for option in options if option.supported]
    if not compatible:
        raise ValueError('No supported Python detected (Django 5.2: 3.10–3.14). Use --python PATH.')
    display_pythons(options)
    if len(compatible) == 1:
        selected = compatible[0]
        print(f'Automatically selected the only compatible interpreter: {selected.executable}')
        return selected

    if interactive is None:
        interactive = sys.stdin.isatty()
    if not interactive:
        raise ValueError('Several compatible Pythons detected. Select one with --python PATH.')

    indices = {index: option for index, option in enumerate(options, 1)}
    while True:
        try:
            answer = reader('Choose the number of the Python to use: ').strip()
        except (EOFError, KeyboardInterrupt) as exc:
            raise ValueError('Python selection cancelled.') from exc
        try:
            option = indices[int(answer)]
        except (ValueError, KeyError):
            print('Enter one of the listed numbers.')
            continue
        if option.supported:
            return option
        print('That Python version is not supported for this Django project.')


def run_stage(label, argv):
    """Stop immediately at a failed, named stage; do not conceal its exit code."""
    print(f'RUNNING: {label}', flush=True)
    try:
        result = subprocess.run(argv, cwd=BACKEND, check=False)
    except OSError as exc:
        print(f'FAILED: {label} ({exc})', file=sys.stderr)
        return False
    if result.returncode:
        print(f'FAILED: {label} (exit {result.returncode})', file=sys.stderr)
        return False
    print(f'PASSED: {label}', flush=True)
    return True


def install(selected, *, skip_install=False):
    """Use the chosen Python only to create the isolated development environment."""
    venv = BACKEND / '.venv'
    local_python = venv / (
        'Scripts/python.exe' if os.name == 'nt' else 'bin/python'
    )
    if not venv.exists() and not run_stage(
        'Create virtual environment',
        [selected.executable, '-m', 'venv', str(venv)],
    ):
        return False
    if not local_python.is_file():
        print('FAILED: Existing .venv is incomplete; inspect it rather than overwriting.',
              file=sys.stderr)
        return False
    installed = probe_python(local_python)
    if installed is None or installed.version[:2] != selected.version[:2]:
        print('FAILED: Existing .venv uses a different or unrecognised Python. '
              'It will not be replaced automatically.', file=sys.stderr)
        return False

    stages = []
    if not skip_install:
        stages.append((
            'Install dependencies in .venv',
            [str(local_python), '-m', 'pip', 'install', '--disable-pip-version-check',
             '-r', str(BACKEND / 'requirements.txt')],
        ))
    stages.extend((
        ('Static checks', [str(local_python), 'scripts/verify.py']),
        ('Installer and preflight tests', [
            str(local_python), '-m', 'unittest', 'discover', '-s', 'scripts',
            '-p', 'test_*.py', '-v',
        ]),
        ('Django checks, migrations and tests', [
            str(local_python), 'scripts/verify.py', '--full',
        ]),
    ))
    for label, command in stages:
        if not run_stage(label, command):
            return False
    print('SUCCESS: All setup and Django validation stages passed.')
    print('No web server or agents were started.')
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--python', help='Path or command name of a specific Python.')
    parser.add_argument('--list-pythons', action='store_true',
                        help='List detected Python interpreters without installing.')
    parser.add_argument('--skip-install', action='store_true',
                        help='Re-run checks in an already installed virtual environment.')
    options = parser.parse_args(argv)

    if options.list_pythons:
        detected = discover_pythons()
        display_pythons(detected)
        return 0 if detected else 1

    try:
        selected = select_python(discover_pythons() if not options.python else [],
                                 requested=options.python)
    except ValueError as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        return 2

    print(f'Chosen Python: {".".join(map(str, selected.version))} '
          f'({selected.executable})')
    return 0 if install(selected, skip_install=options.skip_install) else 1


if __name__ == '__main__':
    raise SystemExit(main())

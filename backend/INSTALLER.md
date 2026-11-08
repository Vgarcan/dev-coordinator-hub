# Local Django installer — Python discovery and validation

## Table of contents

1. [Purpose](#purpose)
2. [Python selection](#python-selection)
3. [Run](#run)
4. [Validation and boundaries](#validation-and-boundaries)

## Purpose

`scripts/setup_local.py` bootstraps and checks the **local development**
Django app. It does not deploy a web service or connect model agents. Run
from any directory with an available Python 3 interpreter. Python 3.13 is
preferred for this repository; Django 5.2 supports Python 3.10–3.14.

## Python selection

The installer probes common `python`/`python3.X` executables on PATH, the
base interpreter running the script, and Windows Python Launcher entries
(`py -0p`) where available. It displays detected versions and actual
executable paths. Distinct paths remain distinct choices even if they use
the same version; aliases to the same interpreter are deduplicated.

- With **multiple compatible** installations and an interactive terminal, it
  asks which numbered interpreter to use.
- With **one compatible** installation, it automatically selects that one.
- With multiple choices in a noninteractive shell, it fails with guidance to
  supply `--python`, instead of guessing.
- With an interpreter outside PATH, supply its absolute path via `--python`.
- Unsupported versions are shown as such and cannot be selected.

## Run

From the project root on Linux or macOS:

```bash
python3 backend/scripts/setup_local.py --list-pythons
python3 backend/scripts/setup_local.py
# Unattended or explicit choice:
python3 backend/scripts/setup_local.py --python /usr/bin/python3.13
```

From Windows PowerShell:

```powershell
py -3.13 backend/scripts/setup_local.py --list-pythons
py -3.13 backend/scripts/setup_local.py
# Supply the actual path shown in the listing when needed:
py -3.13 backend/scripts/setup_local.py --python "C:\\Path\\To\\python.exe"
```

To re-run tests without contacting the package index after first setup:

```bash
python3 backend/scripts/setup_local.py --skip-install --python /usr/bin/python3.13
```

## Validation and boundaries

Stages stop on their first failure and report its name: isolated `.venv`,
dependency install, source checks, standard-library tests, and full Django
system/migration/test verification through existing `scripts/verify.py`.

No global pip, root privileges, GitHub Actions, auto-merge, or agent runtime
is involved. The installer **will not replace** an existing incompatible or
broken `.venv`. The full verifier applies migrations to ignored
`backend/db.sqlite3` locally: do not run against shared/production storage.

This code requires a real Python/Django environment for end-to-end validation.
Its own interpreter-selection tests can run with only the standard library.

# Backend validation — Dev Coordination Hub

Date: 2026-11-08. Runtime acceptance remains **OPEN**.

## Contents

1. What was verified
2. What is still blocked
3. Commands for repeatable local validation

## What was verified

- GitHub source inspection confirmed config, dashboard, repositories, and a handwritten initial migration in main.
- The staff-only inventory decorator and corresponding tests were inspected, **not executed**.
- The standalone validation helper was compiled with Python 3.13 and self-tested against temporary fixture files. Those files were NOT the actual project checkout.
- The static GitHub Pages site is separate from the Django backend.

## What is still blocked

- The actual Django app has NOT passed manage.py check, migration drift verification, migrate or test.
- The Python 3.13 environment has no Django package. Its package index is inaccessible; a pip install attempt listed no available versions.
- The initial migration **must** pass the Django migration autodetector before it can be considered validated.

## Commands for repeatable local validation

After cloning main, enter backend and install requirements in a Python 3.13 virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify.py
python scripts/verify.py --full
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` before running the Python commands. Alternatively use the explicit setup in backend/README.md.

Normal mode uses only the Python standard library and checks source syntax and expected paths. Full mode additionally runs Django checks, migration drift detection, migrate and Django tests. It supplies an ephemeral development SECRET_KEY if none is set.

**Warning:** full mode applies migrations to the local, ignored backend/db.sqlite3. Do not use it against a shared/production database.

Link passing command output to Issue #11. Do not claim runtime success until it actually passes on an installed Django environment.

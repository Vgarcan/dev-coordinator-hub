# Backend validation — Dev Coordination Hub

Last updated: 2026-11-09. Local runtime gates **PASSED** on Linux; formal
acceptance remains **pending owner review** (Issue #11). Related requirement:
FR-01 (local repository inventory foundation only; no agent execution).

## Contents

1. Local runtime run — 2026-11-09
2. Earlier source-only review — 2026-11-08
3. Still open
4. Commands for repeatable local validation

## Local runtime run — 2026-11-09

Environment: RHEL 9-compatible Linux, distro-packaged **Python 3.12.15**
(Python 3.13, the preferred version, was not installed on the host;
Django 5.2 supports 3.10–3.14). Fresh `backend/.venv`, no `backend/.env`.

Command, from the repository root (non-interactive shell, so the
interpreter was passed explicitly):

```bash
python3.12 backend/scripts/setup_local.py --python /usr/bin/python3.12
```

Installer result: `SUCCESS`, exit code 0. Every stage passed:

| Stage | Result |
| --- | --- |
| Create virtual environment | PASSED |
| Install dependencies | PASSED — Django 5.2.19, python-dotenv 1.2.4, asgiref 3.13.0, sqlparse 0.6.1 |
| Static checks (`scripts/verify.py`) | PASSED — 35 Python files parsed, required files present |
| Installer and preflight tests | PASSED — 33 tests |
| `manage.py check` | No issues (0 silenced) |
| `makemigrations --check --dry-run` | No changes detected — the handwritten `repositories/0001_initial.py` matches the models |
| `migrate --noinput` | All admin, auth, contenttypes, repositories and sessions migrations applied to the ignored local `db.sqlite3` |
| `manage.py test` | PASSED — 58 tests |

The `FAILED: Sample failure (exit 4)` lines in the output are expected: they
are printed by `test_failed_stage_reports_false`, which checks that a failing
stage is reported, and that test passes.

Additional manual checks after the installer:

- `git status` stayed clean; only ignored paths were created (`.venv/`,
  `db.sqlite3`, `__pycache__/`).
- `pip check` inside `.venv`: no broken requirements.
- `scripts/preflight.py`: Django importable; reports
  `Python 3.13 recommended match: False` (3.12 was used).
- Loopback smoke test of `runserver` on `127.0.0.1` with an ephemeral secret
  key and `DJANGO_DEBUG=1`, stopped afterwards:

| Path | Response |
| --- | --- |
| `/`, `/tasks/`, `/agents/` | 200, with the expected page titles |
| `/admin/login/` | 200 |
| `/admin/`, `/repositories/` (anonymous) | 302 to `/admin/login/?next=…` |
| `/static/dashboard/css/app.css`, `tasks.css`, `agents.css` | 200 |
| Unknown path | 404 |

## Earlier source-only review — 2026-11-08

- GitHub source inspection confirmed config, dashboard, repositories, and a
  handwritten initial migration in main.
- The staff-only inventory decorator and its tests were inspected, not
  executed. They have since passed in the 2026-11-09 run.
- The standalone validation helper was compiled with Python 3.13 and
  self-tested against temporary fixtures. At that time, the package index was
  not reachable and Django could not be installed, so the runtime gates were
  blocked.
- The static GitHub Pages site is separate from the Django backend.

## Still open

- **Python 3.13 run:** the passing run used 3.12. Repeat with 3.13 if that
  version must be the reference.
- **Windows run:** `py -3.13 backend/scripts/setup_local.py` has not been
  exercised in this evidence.
- **Browser rendering:** no visual or responsive inspection was done. The
  Glassmorphism Pro theme stylesheet loads from an external host and was not
  checked.
- **Staff inventory in a real session:** no superuser was created; the
  `/repositories/` staff path is covered by tests only.
- **Duplicate test discovery:** `manage.py test` also collects the 33
  `scripts/test_*.py` tests (because `scripts` is a package), so they run in
  both stages. This is harmless and does not change the result.
- Acceptance stays pending until an attributable owner review on Issue #11.

## Commands for repeatable local validation

Preferred: the [guided installer](INSTALLER.md), which runs every stage above.

Manual alternative — from `backend`, in a Python 3.10–3.14 virtualenv
(3.13 preferred):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/verify.py
python scripts/verify.py --full
```

On Windows PowerShell, activate with `.\.venv\Scripts\Activate.ps1` before
running the Python commands. Alternatively use the explicit setup in
backend/README.md.

Normal mode uses only the Python standard library and checks source syntax and
expected paths. Full mode also runs Django checks, migration drift detection,
migrate and the Django tests. It supplies an ephemeral development SECRET_KEY
if none is set.

**Warning:** full mode applies migrations to the local, ignored
backend/db.sqlite3. Do not use it against a shared or production database.

Link passing command output to Issue #11. Do not claim runtime success for an
environment that has not actually passed these commands.

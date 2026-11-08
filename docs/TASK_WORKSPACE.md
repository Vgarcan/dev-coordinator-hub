# Fictional Django task workspace

## Table of contents

1. [Purpose](#purpose)
2. [Implementation](#implementation)
3. [Validation](#validation)
4. [Operational boundary](#operational-boundary)

## Purpose

The `/tasks/` page is a presentation-only demonstration of the proposed
development-task lifecycle. It is **not** the coordinator or a live control UI.

## Implementation

- `dashboard/views.py`: four hard-coded, invented example tasks and an
  allowlisted GET status filter; no database reads or writes.
- `dashboard/urls.py`: standard Django route `dashboard:tasks`.
- `dashboard/templates/dashboard/tasks.html`: shared base layout, status
  selection, count, empty state and an explainer of approval boundaries.
- `dashboard/templates/dashboard/_task_card.html`: repeated accessible card.
- `dashboard/static/dashboard/css/tasks.css`: mobile-first view-specific CSS
  loaded through `base.html`'s existing `extra_css` block.
- `backend/templates/partials/_nav_links.html`: same URL in desktop and
  mobile navigation; page-specific active state.

No new Django app, dependency, JavaScript bundle or migration was required.

## Validation

`DashboardTaskDemoTests` checks rendering, server-side filtering, unknown
status handling, empty states and absence of write controls. Run from
`backend/` after installing Django with `python scripts/verify.py --full`.
Runtime and browser tests must not be claimed passed until actually run.

## Operational boundary

All sample identifiers and repository names are fictional. This route does
not read private GitHub data, execute CLIs, request credentials or approve
work. The future authorisation and execution protocol remains subject to the
separate security and feasibility gates in `docs/PDD.md` and
`docs/TASK_PROTOCOL.md`. GitHub Pages remains a static standalone prototype.

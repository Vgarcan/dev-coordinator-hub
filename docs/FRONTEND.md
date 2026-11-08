# Django frontend architecture — reusable templates and Glassmorphism Pro

**Status:** initial shared UI implementation; Django runtime and browser visual tests are not yet executed. Tracked in Issue #12.

## Table of contents

1. [Objective](#objective)
2. [Templates and partials](#templates-and-partials)
3. [Theme contract and asset order](#theme-contract-and-asset-order)
4. [Mobile-first and accessibility](#mobile-first-and-accessibility)
5. [How to add a page](#how-to-add-a-page)
6. [Validation and boundaries](#validation-and-boundaries)

## Objective

Make the local Django frontend navigable and maintainable while preserving a familiar **vanilla Django** project. Templates share their HTML shell and components; each app owns its own page content. The existing GitHub Pages concept remains untouched.

## Templates and partials

| Location | Responsibility |
| --- | --- |
| `backend/templates/base.html` | Shared document, CSS includes, content blocks, landmarks |
| `backend/templates/partials/_site_header.html` | Site branding with independently visible desktop and mobile navigation |
| `backend/templates/partials/_nav_links.html` | One source for nav destinations/active-page state |
| `backend/templates/partials/_feature_tile.html` | Reusable editorial feature tile on overview |
| `backend/templates/partials/_status_strip.html` | Static non-operational status disclaimer |
| `backend/templates/partials/_site_footer.html` | Small common footer |
| `backend/dashboard/templates/dashboard/home.html` | Django home/overview |
| `backend/repositories/templates/repositories/list.html` | Staff-only inventory page and empty state |
| `backend/repositories/templates/repositories/_repository_card.html` | Reusable, presentation-only repository card |
| `backend/dashboard/static/dashboard/css/app.css` | App-only presentation and responsive adjustments |

The project-level `TEMPLATES[0]['DIRS']` adds `BASE_DIR / 'templates'`; default `APP_DIRS=True` remains. No custom template loader, frontend framework or bundler is added.

## Theme contract and asset order

The separate [Bootstrap theme collection](https://github.com/Vgarcan/botstrap-css-styles) defines [13 semantic `--theme-*` tokens](https://github.com/Vgarcan/botstrap-css-styles/blob/main/docs/THEME_CONTRACT.md). We load:

1. Bootstrap CSS 5.3.
2. **Exactly one upstream** Glassmorphism Pro stylesheet.
3. Our namespaced `dc-*` adjustments via Django's `{% static %}` template tag.

The app does **not** fork, rewrite or relicense the original theme. When updating its upstream design, edit the theme repository, not a duplicated stylesheet here. The Django custom CSS references the semantic contract and adds a small set of local presentation tokens. Optional Glassmorphism JS is intentionally excluded initially: the original CSS already supplies the complete visual identity and the site navigation needs no JavaScript.

The upstream CSS and Bootstrap are loaded from public CDNs. Development with no internet can use the application CSS fallback, but will not reproduce the complete theme. Pin/vendor external assets with a reviewed dependency policy before production deployment.

## Mobile-first and accessibility

- Desktop links live in a separate, ordinary `<nav>` and are never descendants of a closed `<details>` (which would hide them). The mobile `<details>`/`<summary>` remains keyboard-operable without JavaScript; both containers include the same `_nav_links.html`.
- A skip-to-main link, semantic header/nav/main/footer, keyboard focus styles and `aria-current` identify navigation and location.
- Grid layout begins as one column, expanding at 768 px; tiny phone widths use wrapped or full-width controls.
- Editorial serif display headings contrast with the unchanged upstream sans-serif body. Added geometric light and layered material details are static (no looping decorative animation).
- Feature tiles and repository cards use template includes only for genuinely repeated markup, not a new component framework.
- Respect `prefers-reduced-motion: reduce`; ornamental pointer tracking is not necessary for usability.
- Repository browsing is still protected by the server-side `staff_member_required` decorator. Hiding links is **not** an authorization mechanism.

## How to add a page

Use `{% extends 'base.html' %}` in a conventional app template; override `title`, `meta_description` and `content` as needed. Put reusable UI sections under `backend/templates/partials/`, and app-specific styles under app static directories. Prefer a shared component only when multiple pages genuinely need it.

Do not paste new `<!doctype html>` boilerplate or repeat Bootstrap/theme links into page templates. Keep class selectors namespaced `dc-*` to avoid accidentally overriding upstream component styles.

## Validation and boundaries

Source-file checks confirm both pages extend `base.html`, shared navigation and card partials are referenced, CSS load order is stable and existing route/test assertions are kept. Issue #13 documents the additional navigation fix and reusable components. **Django `manage.py test` and actual responsive-browser checks are still pending** because Django has not been installed in the execution environment.

This frontend does not execute agents, use GitHub credentials, approve tasks, expose live audits, or alter the static GitHub Pages site.

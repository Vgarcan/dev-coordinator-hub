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
| `backend/templates/partials/_site_header.html` | Site branding and native mobile navigation |
| `backend/templates/partials/_status_strip.html` | Static non-operational status disclaimer |
| `backend/templates/partials/_site_footer.html` | Small common footer |
| `backend/dashboard/templates/dashboard/home.html` | Django home/overview |
| `backend/repositories/templates/repositories/list.html` | Staff-protected repository cards and empty state |
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

- Native `<details>`/`<summary>` supplies a collapsible navigation on narrow viewports without a JavaScript dependency.
- A skip-to-main link, semantic header/nav/main/footer, keyboard focus styles and `aria-current` identify navigation and location.
- Grid layout begins as one column, expanding at 768 px.
- Respect `prefers-reduced-motion: reduce`; ornamental pointer tracking is not necessary for usability.
- Repository browsing is still protected by the server-side `staff_member_required` decorator. Hiding links is **not** an authorization mechanism.

## How to add a page

Use `{% extends 'base.html' %}` in a conventional app template; override `title`, `meta_description` and `content` as needed. Put reusable UI sections under `backend/templates/partials/`, and app-specific styles under app static directories. Prefer a shared component only when multiple pages genuinely need it.

Do not paste new `<!doctype html>` boilerplate or repeat Bootstrap/theme links into page templates. Keep class selectors namespaced `dc-*` to avoid accidentally overriding upstream component styles.

## Validation and boundaries

Source-file checks confirm both pages extend `base.html`, partials exist, CSS load order is stable and existing route/test assertions are kept. **Django `manage.py test` and actual responsive-browser checks are still pending** because Django has not been installed in the execution environment.

This frontend does not execute agents, use GitHub credentials, approve tasks, expose live audits, or alter the static GitHub Pages site.

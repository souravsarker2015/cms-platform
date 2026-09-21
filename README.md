# Endeavours CMS

The company website and CMS for **Endeavours**, built on Wagtail. Editors
manage every part of the public site — pages, navigation, footer, and company
details — from the Wagtail admin.

This is **Phase 1**: project architecture, the reusable design system, and a
fully editable homepage.

---

## Stack

| Layer     | Choice |
|-----------|--------|
| Language  | Python 3.12 |
| Framework | Django 6.1 + Wagtail 8.0 |
| Database  | PostgreSQL (SQLite permitted in staging only) |
| CSS       | Tailwind CSS v4 (standalone CLI) |
| JS        | Alpine.js (interactivity), htmx (partial updates) |
| Config    | `django-environ`, env-based, no secrets in the repo |
| Rendering | Server-rendered Wagtail templates |

---

## Project layout

```
cms-platform/
├── apps/
│   ├── core/          Shared blocks, snippets, base page, template tags
│   │   ├── blocks.py            Reusable StreamField blocks
│   │   ├── models.py            BasePage, SiteSettings, Navigation, Footer
│   │   ├── context_processors.py
│   │   └── templatetags/
│   ├── home/          HomePage
│   └── pages/         StandardPage (About, Services, …)
├── endeavours/
│   ├── settings/      base / dev / staging / production
│   ├── static/        Compiled CSS, vendored JS, fonts
│   ├── templates/     base.html, includes/, error pages
│   └── urls.py
├── frontend/
│   └── main.css       Tailwind source (design tokens + components)
├── requirements/      base / dev / production
├── search/            Site search
├── Makefile
└── .env.example
```

Apps stay decoupled: `home` and `pages` depend on `core`, never on each other.

---

## Setup

Requires Python 3.12, Node 18+, and PostgreSQL.

```bash
# 1. Clone, then create the virtualenv and install everything
make install

# 2. Create your .env from the example, then edit the database credentials
make env

# 3. Create the database (adjust to your local Postgres setup)
createdb wagtail_cms

# 4. Apply migrations — this also creates the homepage
make migrate

# 5. Build the stylesheet and vendored JS
make css

# 6. Create the admin user and load demo content
make seed

# 7. Run it
make run
```

The site is at <http://localhost:8000> and the admin at
<http://localhost:8000/admin/>.

`make seed` creates a superuser and fills the site with representative
content. The default development credentials are:

| Username | Password |
|----------|----------|
| `admin`  | `admin123456` |

> **These are local development credentials.** Change the password before the
> site is reachable by anyone else. Override them with `SEED_ADMIN_USERNAME` /
> `SEED_ADMIN_PASSWORD`, with the `--admin-username` / `--admin-password`
> flags, or skip the user entirely with `--skip-admin` and use
> `make superuser`.

New to the admin? See **[user_guide.md](user_guide.md)** for a walkthrough
written for non-technical editors.

While working on templates or styles, run `make css-watch` in a second
terminal to rebuild the stylesheet on save.

### Configuration

All configuration comes from the environment. `make env` copies
`.env.example` to `.env` for you; fill in the database credentials. Both `.env`
and any `.env.*` variant are git-ignored and must never be committed — only
`.env.example` is tracked.

The local database defaults to `wagtail_cms`:

```
DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/wagtail_cms
```

`SECRET_KEY` has an insecure default in **dev only**. Staging and production
both require it to be set explicitly, and will refuse to start without it.

Generate one with:

```bash
python -c "from django.core.management.utils import get_random_secret_key as k; print(k())"
```

### Settings modules

| Module | Purpose |
|--------|---------|
| `base.py` | Shared configuration. Imported by the rest; never used directly. |
| `dev.py` | Local development. `DEBUG=True`, console email, debug toolbar. **Default.** |
| `staging.py` | Mirrors production but allows SQLite for a throwaway database. |
| `production.py` | `DEBUG=False`, HSTS, secure cookies, WhiteNoise, SMTP, required secrets. |

Select one with `DJANGO_SETTINGS_MODULE` or `--settings`:

```bash
python manage.py check --settings=endeavours.settings.production
```

---

## Content architecture

### Pages

- **`BasePage`** (abstract, in `core`) — every page inherits its SEO fields:
  meta title, meta description, Open Graph title/description/image, and a
  `noindex` toggle. Pages default to appearing in menus
  (`show_in_menus_default = True`).
- **`HomePage`** — hero (heading, subheading, image, buttons), a StreamField
  body, and a closing call to action. Limited to one instance at the site root.
- **`StandardPage`** — intro text plus StreamField body. Used for About,
  Services, and similar. Can nest.

### Blocks

Defined once in `apps/core/blocks.py` and available in any page body:

| Block | Purpose |
|-------|---------|
| **Hero** | Page-opening banner, optional background image |
| **Rich text** | Prose with a deliberately limited feature set |
| **Image** | Image with caption, attribution, and width options |
| **Feature grid** | Icon/title/text cards in 2–4 columns |
| **Call to action** | Heading, text, and up to two buttons |
| **Testimonial** | Quote with author and optional logo |
| **Stats** | Up to four headline figures |
| **FAQ** | Accordion, expand/collapse via Alpine.js |
| **Button** | Links to an internal page *or* an external URL |

The **Button** block resolves internal pages and external URLs behind one
interface, so editors never hand-write a URL to their own site. A page link
always wins over an external URL, and link text falls back to the page title.

### Snippets and settings

Editable from the admin, no deploy required:

- **Site settings** (Settings → Site settings) — company name, tagline, logos,
  favicon, contact email/phone/address, social links, default share image.
- **Navigation menus** (Snippets) — named, ordered, two levels deep. The menu
  with slug `main` renders in the header.
- **Footer** (Snippets) — intro blurb, link columns, legal links, copyright.

Navigation and footer reach every template through
`apps.core.context_processors.navigation`. The site renders correctly when
none of them are configured yet.

---

## Design system

Tokens live in `frontend/main.css` as CSS variables, so they are available to
both Tailwind utilities and hand-written CSS.

- **Colour** — `primary` (blue), `secondary` (slate), `accent` (amber), each a
  full 50–950 ramp defined in OKLCH for even perceptual steps.
- **Type** — Inter, self-hosted as a variable font (one request, weights
  100–900), with `font-display: swap` and a preload hint.
- **Scale** — a restrained type scale from `xs` to `6xl`, each with a paired
  line height.
- **Components** — `.btn` (primary/secondary/ghost), `.card`, `.section`,
  `.container-site`, `.icon-tile`, `.nav-link`, `.eyebrow`.

### Accessibility

Built in rather than retrofitted:

- Semantic landmarks (`header`, `nav`, `main`, `footer`) and a skip link.
- A single visible `:focus-visible` outline everywhere; focus is never removed.
- Accordions and dropdowns use `aria-expanded` / `aria-controls`, with ids
  derived from content so they stay stable across requests.
- Interactive targets meet the 44px minimum.
- `prefers-reduced-motion` disables transitions and smooth scrolling.
- Background images always sit behind a scrim so text keeps its contrast.

---

## Commands

```
make help          List every target
make install       Install Python + Node dependencies
make env           Create .env from the example
make migrate       Apply migrations
make superuser     Create an admin user
make seed          Create the admin user and load demo content
make run           Start the dev server
make css           Build the stylesheet (minified)
make css-watch     Rebuild the stylesheet on change
make static        Collect static files for deployment
make test          Run the test suite
make lint          Check lint and formatting
make format        Apply autofixes
make reset-db      Drop, recreate, migrate and seed the database
```

---

## Testing

```bash
make test
```

22 tests cover block link resolution and validation, stable FAQ ids, site
settings helpers, navigation fallbacks, the context processor (including a
site with no menu or footer configured), page rendering, SEO defaults, and
that every block renders.

The suite creates and drops its own test database, so it needs a Postgres user
with `CREATEDB`. It is verified against PostgreSQL 16.

---

## Deployment notes

1. Install production dependencies: `make install-prod`.
2. Set every variable from `.env.example` in the environment. `SECRET_KEY` and
   `ALLOWED_HOSTS` are **required** and have no defaults.
3. Build assets: `npm ci && npm run build`, then `make static`.
4. Run migrations: `python manage.py migrate`.
5. Serve with `gunicorn endeavours.wsgi:application`.

Static files are served by WhiteNoise with compression and content hashing, so
no separate static file server is needed. Production enables HSTS, secure
cookies, `SECURE_SSL_REDIRECT`, and `X-Frame-Options: DENY`; it expects to sit
behind a TLS-terminating proxy that sets `X-Forwarded-Proto`.

Verify a deployment config before shipping:

```bash
python manage.py check --deploy --settings=endeavours.settings.production
```

---

## Phase 1 scope

**Included:** project architecture, split settings, the design system, the
block library, editable navigation/footer/site settings, HomePage,
StandardPage, site search, error pages, and tests.

**Not included** (later phases): blog and case studies, contact forms,
multi-language support, and a caching layer.

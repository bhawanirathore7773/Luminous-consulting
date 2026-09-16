# SAP Consulting Platform — Complete (Phases 1–7)

Django + Tailwind build of the full production spec, swapped from the
spec's default Next.js/TypeScript stack per your Python/Django background.
All 7 phases are done:

1. Scaffold, design system, homepage
2. `services` — 14 service pages
3. `solutions` (6) + `industries` (12)
4. SAP Expertise, case studies (5 representative use cases), team
5. Insights knowledge center (6 articles, search + category filter)
6. SAP assessment wizard + contact/lead capture
7. About index, Approach (6-step methodology), Careers, 5 legal pages,
   sitemap.xml, robots.txt

## What's in Phase 1

- Django project (`sap_platform`) with a `core` app
- Design system: color tokens, type scale, restrained border-radius, in
  `core/static/core/css/src/input.css` + `tailwind.config.js`
- Sticky header with mega-menus (Services / Solutions / Industries), footer,
  and a reusable Button component (`{% button %}` template tag)
- Homepage: hero (with an original SVG SAP-landscape diagram), capability
  strip, interactive problem selector, services teaser, outcome pillars,
  closing CTA

## What's in Phase 2

- `services` app: `Service` model + `ServiceListItem` (one model, tagged by
  section, instead of four near-identical list models) + a generic `FAQ`
  model in `core` (attaches to any model via `GenericForeignKey` — solutions
  and industries reuse it in later phases instead of each getting their own)
- `/services/` index and `/services/<slug>/` detail pages, covering all 14
  pages from Section 10 (SAP Consulting, S/4HANA, Implementation, Migration,
  Integration, BTP, Development, AMS & Support, Managed Services, Support,
  Security, Data & Analytics, Testing, Training)
- Reusable detail-page partials in `core/templates/core/partials/`
  (`detail_hero`, `text_section`, `list_section`, `faq_section`,
  `related_grid`) — Phase 3's Solutions/Industries apps reuse these directly
- `python manage.py seed_services` populates all 14 services with real,
  concise content (business problem, capabilities, technology, deliverables,
  FAQs, related-service links) — safe to re-run, upserts by slug
- The homepage's services teaser now pulls from the database
  (`Service.objects.filter(featured=True)`) instead of hardcoded data
- schema.org `Service` JSON-LD on every detail page (Section 28)

## What's in Phase 3

- `solutions` app: `Solution` model, business-problem-framed (Section 11's
  distinction — services are *what we do*, solutions are *the problem we
  solve*). Each solution cross-links to the specific `Service` objects that
  deliver it via a real M2M, not duplicated copy.
- `industries` app: `Industry` model covering all 11 blocks Section 12
  requires (challenges, processes, SAP landscape, modules, integration
  needs, transformation opportunities, use cases, related services,
  outcomes, FAQs, CTA) — genuinely differentiated per industry (distinct
  SAP modules, integration needs, and use cases for each), not one template
  with the industry name swapped in.
- `python manage.py seed_solutions` — 6 solutions (SAP Transformation,
  Modernization, Cloud Transformation, Integration, Automation, Data & AI)
- `python manage.py seed_industries` — all 12 industries from Section 12
- Homepage now shows a live "Industries we work with" section
- All 32 CTAs across services + solutions + industries are distinct
  (Section 23: never the same CTA everywhere) — verified, not just written
  that way by hand

## What's in Phase 4

- `sap_expertise` app: a single `/sap-expertise/` page (Section 13
  deliberately defers individual technology/module pages to later). Seed
  data is limited to platforms, technologies, and modules **already
  referenced** in the seeded services/industries content — SuccessFactors,
  Ariba, and HCM appear in the spec's example list but aren't backed by
  anything built so far, so they're left out rather than claimed unearned.
- `case_studies` app: 5 representative SAP use cases at `/case-studies/`
  and `/case-studies/<slug>/`, matching Section 18's exact 9-block format
  (Industry, Business challenge, SAP environment, Objective, Approach,
  Solution, Services, Technology, Outcome). Every entry is explicitly
  labeled "Representative SAP use case — not a specific client disclosure"
  on both the card and detail page, and titles describe a business
  archetype ("S/4HANA Conversion for a Discrete Manufacturer") rather than
  a real or invented company name — Section 2 prohibits fabricating client
  credentials, and Section 18 calls for exactly this kind of clear labeling
  when real case studies aren't available.
- `about` app: `/about/team/` (Section 19). **Intentionally seeded with
  zero team members** — inventing named consultants with fabricated
  expertise or certifications is exactly the kind of fake credibility
  Section 2 rules out. The page instead shows the 12 expertise categories
  the practice is organized around; real profiles can be added via
  `/admin/` whenever they exist, and the page renders them automatically
  once at least one is added. The `/about/` index itself (company
  philosophy, leadership, etc.) is still Phase 7 — only `/about/team/` is
  live now.
- Homepage gained a live "Representative use cases" section; footer now
  links to Team and SAP Expertise.

## What's in Phase 5

- `insights` app: `/insights/` (search + category filter) and
  `/insights/<slug>/` (Section 21). Search matches title, summary, and body
  via a plain GET form — no JS required, works with the browser back
  button and is bookmarkable/shareable as a URL.
- `author` defaults to an institutional byline ("SAP Practice Team"), not
  an invented named writer — same reasoning as the empty team page in
  Phase 4. `reading_time_minutes` is computed from word count rather than
  stored, so it can't go stale as content is edited.
- 6 real articles seeded across 6 categories and 3 content types (Article,
  Guide, Checklist) — genuine SAP domain content, not filler text, so
  search and filtering both have something real to demonstrate.
- schema.org `Article` JSON-LD on every detail page, with `author` typed
  as `Organization` rather than `Person` (consistent with there being no
  real named author on file yet).
- All 38 CTAs across services + solutions + industries + insights are
  still distinct — checked, not just written that way by hand.

## What's in Phase 6

- `assessment` app: the 6-step "How Healthy Is Your SAP Landscape?" wizard
  at `/assessment/` (Section 17). Runs entirely client-side (Alpine.js for
  step state, plain JS for the scoring/recommendation logic) — no model,
  no server round-trip per step. The results screen is explicitly labeled
  "not an authoritative SAP audit," per the spec's own instruction not to
  present it as one. **Functionally tested**, not just written and hoped
  to work — ran the actual recommendation logic in Node against three
  different answer profiles (a risky legacy landscape, a moderate one, a
  clean one) and confirmed each produces distinct, sensible attention
  flags and recommendations rather than generic output.
- `leads` app: the contact page (`/contact/`, Section 22) with every
  specified field, a honeypot field for spam protection (Section 31 — no
  CAPTCHA/JS dependency needed for this level), and a thank-you page with
  the exact 4-step next-steps sequence the spec calls for. No response
  time is promised anywhere, per the spec's explicit instruction.
- The two are connected: finishing the assessment links to
  `/contact/?source=assessment&summary=...`, which pre-fills the message
  field and shows a small banner acknowledging the handoff — so a
  completed assessment doesn't dead-end, it flows straight into a real
  lead.
- Homepage gained the assessment CTA section (Section 41's homepage flow,
  item 14 — placed right before the final CTA, as specified).

## What's in Phase 7 (final)

- `/about/` (Section 20) — all 12 subsections, but not all treated the same
  way: Philosophy, How We Work, Delivery Model, Quality, Security, and
  Values are genuine written content. Leadership and Locations get the
  same honest placeholder treatment as the empty team page (Phase 4) —
  no invented executives, no invented office cities, since Section 2
  prohibits fabricating exactly that kind of credential.
- `/approach/` (Section 15) — the six-stage methodology (Discover → Assess
  → Design → Deliver → Stabilize → Optimize), click-to-expand via native
  `<details>`, no JS dependency. This is a genuine sequence, so it's
  numbered — unlike the six parallel outcome pillars on the homepage,
  which deliberately aren't.
- `/careers/` — honest that no specific roles are listed, routes interest
  to `/contact/` rather than fabricating job postings.
- `legal` app: the 5 pages Section 34 requires, admin-editable, seeded
  with generic template content and bracketed placeholders
  (`[Company Name]`, `[jurisdiction]`, etc.) for what's genuinely
  business-specific. Every page shows a visible banner stating it hasn't
  been reviewed by legal counsel — this is a starting point, not
  publish-ready legal text, and Claude has no basis to certify otherwise.
- `sitemap.xml` and `robots.txt`, covering every content type and static
  page across all 7 phases.
- **Audited this round**: cross-referenced every `{% url %}` tag,
  `reverse()` call, and sitemap entry against the actual registered URL
  names — caught and fixed one real bug (`about:careers` referenced a
  namespace that didn't exist, since `/careers/` is a top-level route, not
  nested under `/about/`).

The site is now fully wired — every nav link, footer link, and CTA across
all 7 phases resolves to a real page.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit SITE_NAME, SECRET_KEY, etc.

npm install
npm run build:css      # compiles Tailwind — required before the page looks right

python manage.py makemigrations
python manage.py migrate
python manage.py seed_services      # populates the 14 service pages
python manage.py seed_solutions     # populates the 6 solution pages
python manage.py seed_industries    # populates the 12 industry pages
python manage.py seed_expertise     # populates the SAP Expertise page
python manage.py seed_case_studies  # populates 5 representative use cases
python manage.py seed_insights      # populates 6 insights articles
python manage.py seed_legal_pages   # populates the 5 legal pages
python manage.py createsuperuser    # so you can edit content at /admin/

python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site, `/admin/` to edit content, and
`/admin/leads/lead/` to see submitted contact requests (including which
came from the assessment wizard via the `source` field). There's no
`seed_team` command by design (see Phase 4 above) — add real team members
directly in `/admin/` and they'll appear on `/about/team/` automatically.

For local dev, `.env`'s default `DATABASE_URL` is SQLite (zero setup). Point
it at Postgres when you're ready — no code changes needed, just the env var.

While iterating on styles: `npm run watch:css` rebuilds on save.

**Note on the contact form's spam protection:** the honeypot field is a
solid first layer with zero dependencies, but a production deployment
should add rate limiting (e.g. `django-ratelimit`) in front of the contact
view too — that's a one-line decorator once the package is installed, left
out here only because this sandbox has no network access to install and
test it.

## What to do before this goes live

Everything above is real, working code — but a few things are
deliberately left as placeholders because inventing them would mean
fabricating facts about a real business, which none of this build has
done anywhere:

- **Company identity**: `SITE_NAME` in `.env`, plus the bracketed
  placeholders in the 5 legal pages (`[Company Name]`, `[jurisdiction]`,
  contact emails)
- **Legal review**: every legal page shows a visible "not reviewed by
  counsel" banner until a real lawyer signs off
- **Team profiles**: add real people via `/admin/` — `/about/team/` picks
  them up automatically
- **Office locations**: the About page's Locations section is
  intentionally vague until real ones are confirmed
- **Real case studies**: swap in actual client work via `/admin/` once
  you have permission to publish it, replacing (or supplementing) the 5
  representative use cases
- **Rate limiting** on the contact form (see the setup note above)

Everything else — content models, the design system, all 7 phases of
pages, search, the assessment wizard, the sitemap — is ready to run as-is.



## Deployment hardening added

The repository now includes:

- Dockerfile with a reproducible Python + Tailwind multi-stage build.
- docker-entrypoint.sh for database initialization, deployment checks, optional seed data, and Gunicorn.
- render.yaml for a Render Web Service + PostgreSQL Blueprint.
- /healthz/ readiness endpoint for Render health checks.
- Production-safe reverse-proxy/HTTPS settings for Render and nginx/Hostinger.
- GitHub Actions CI for Tailwind build, Django checks, deployment checks, migrations, tests, and collectstatic.
- .dockerignore to keep the production image small.

### Render

Use the repository's render.yaml as a Blueprint. Render supports Docker services and Blueprint-managed databases. The app listens on Render's $PORT and exposes /healthz/ for readiness.

For the first deployment, RUN_SEED_DATA=true loads the supplied service, solution, industry, expertise, case-study, insight, and legal seed content. After you have edited production content in /admin/, set RUN_SEED_DATA=false so deployments do not re-seed content.

Important: the current repository does not contain committed Django migration files for the custom apps. The Docker entrypoint uses migrate --run-syncdb so the current database can bootstrap, but this is a deployment bridge, not the preferred long-term migration strategy. Before making schema changes in production, run python manage.py makemigrations locally and commit the generated migrations/ directories. Django recommends keeping migration files in version control.

Render's Free Postgres is suitable for testing/preview, but current Render documentation says Free Postgres expires after 30 days and has no backups. Use a paid database for persistent production data.

### Hostinger VPS

The same Docker image can be run on a Hostinger VPS, or the project can be installed directly with Python + Gunicorn + nginx. For a VPS, keep:

1. DEBUG=False
2. DJANGO_SECRET_KEY in environment variables
3. DATABASE_URL pointed at PostgreSQL
4. ALLOWED_HOSTS set to the real domain
5. CSRF_TRUSTED_ORIGINS set to the HTTPS origin when required
6. nginx terminating TLS and proxying to Gunicorn
7. committed Django migrations applied with python manage.py migrate
8. python manage.py collectstatic --noinput

### Local preflight

    python manage.py check
    python manage.py check --deploy
    python manage.py makemigrations
    python manage.py migrate
    python manage.py test --verbosity 2
    python manage.py collectstatic --noinput

For production, do not use python manage.py runserver; use Gunicorn behind the platform/web server.

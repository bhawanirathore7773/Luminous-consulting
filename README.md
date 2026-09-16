# SAP Consulting Platform — Complete (Phases 1–7)

Django + Tailwind build of the full production spec, swapped from the spec's default Next.js/TypeScript stack per your Python/Django background. All 7 phases are done.

## Deployment

Use `gunicorn sap_platform.wsgi:application` for production. Run `python manage.py collectstatic --noinput` during deployment. Configure `DJANGO_SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `DATABASE_URL` from `.env.example` in the hosting environment.

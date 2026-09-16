#!/bin/sh
set -eu

echo "==> Applying Django migrations"
python manage.py migrate --run-syncdb --noinput

echo "==> Running deployment checks"
python manage.py check --deploy

if [ "${RUN_SEED_DATA:-false}" = "true" ]; then
  echo "==> Loading initial content"
  python manage.py seed_services
  python manage.py seed_solutions
  python manage.py seed_industries
  python manage.py seed_expertise
  python manage.py seed_case_studies
  python manage.py seed_insights
  python manage.py seed_legal_pages
fi

echo "==> Starting Gunicorn"
exec gunicorn sap_platform.wsgi:application \
  --bind 0.0.0.0:${PORT:-10000} \
  --workers ${WEB_CONCURRENCY:-2} \
  --timeout ${GUNICORN_TIMEOUT:-120} \
  --access-logfile -

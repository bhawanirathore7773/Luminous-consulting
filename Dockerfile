# syntax=docker/dockerfile:1

# Build Tailwind CSS in an isolated Node stage. The complete source tree is
# copied before the Tailwind build so its content globs can discover every
# Django template and generate the utility classes used by the UI.
FROM node:20-alpine AS assets
WORKDIR /build
COPY package.json ./
COPY tailwind.config.js ./
COPY core/static/core/css/src ./core/static/core/css/src
COPY . .
RUN npm install --no-audit --no-fund
RUN npm run build:css

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PORT=10000

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
COPY --from=assets /build/core/static/core/css/dist/styles.css /app/core/static/core/css/dist/styles.css

RUN python manage.py collectstatic --noinput

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 10000

ENTRYPOINT ["/app/docker-entrypoint.sh"]

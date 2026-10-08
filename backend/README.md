# Luminous Consulting — NestJS backend

This backend is the migration target for the original Django application.

## Stack

- Node.js 22+
- NestJS
- Prisma ORM
- MySQL
- React/Vite frontend served by NestJS in production

## Local setup

1. Create MySQL database.
2. Copy `.env.example` to `.env` and set `DATABASE_URL`.
3. Install dependencies:

```bash
npm install
```

4. Generate the Prisma client:

```npm run prisma:generate
```

5. Export the canonical Django seed content once:

```bash
npm run prisma:source-export
```

This reads the existing Django management-command seed files and writes JSON under `backend/prisma/source-data/`. It is a migration utility only; the Django application remains untouched.

6. Apply the MySQL schema using Prisma migrations when migration files are present:

```bash
npm run prisma:migrate
```

7. Import the migrated content:

```bash
npm run prisma:seed
```

8. Build:

```bash
npm run build
```

9. Start:

```bash
npm run start:prod
```

## Production architecture

For the easiest Hostinger deployment, build the frontend first and let NestJS serve `frontend/dist` from the same Node application. This keeps the public site and `/api` on one domain and avoids a separate frontend server.

Required production environment variables:

- `NODE_ENV=production`
- `PORT` — Hostinger-provided Node application port
- `DATABASE_URL=mysql://USER:PASSWORD@HOST:3306/DATABASE`
- `PUBLIC_URL=https://your-domain.example`
- `CORS_ORIGIN=https://your-domain.example`

## Safety

The original Django `main` branch is the rollback source. Do not delete or rewrite it until the migrated application has passed visual, URL, form, database, SEO and production smoke tests.

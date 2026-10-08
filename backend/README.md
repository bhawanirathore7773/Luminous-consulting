# Luminous Consulting — NestJS + Prisma + MySQL migration

This branch is the safe migration target for the existing Django site.

## Stack
- Node.js
- NestJS
- Prisma ORM
- MySQL
- Existing Tailwind CSS design system and content preserved as the source of truth

## Hostinger deployment target
The backend is designed for a Node.js application environment:
1. Create a MySQL database in Hostinger.
2. Set `DATABASE_URL` and production environment variables.
3. Run `npm install`.
4. Run `npm run prisma:generate`.
5. Run `npm run prisma:migrate`.
6. Run `npm run prisma:seed` for the initial content load.
7. Run `npm run build`.
8. Start with `npm run start:prod`.

Never commit real `.env` values or database credentials.

## Migration safety
The original Django `main` branch remains unchanged. This branch is the migration sandbox and can be compared with `main` before any production cutover.

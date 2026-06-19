# Django Admin Inventory System

This project turns the Django admin into a complete internal inventory application with:

- product list customization with a computed stock status badge
- a clearance admin action that writes audit logs atomically
- a custom admin dashboard at `/admin/inventory/dashboard/`
- row-level edit permissions based on the user profile category
- read-only stock audit inlines on product change pages
- Docker Compose support with PostgreSQL and startup seeding

## Run with Docker

1. Copy `.env.example` to `.env` and adjust values if needed.
2. Start the stack:

```bash
docker-compose up --build -d
```

3. Open `http://localhost:8000/admin/`.

## Seeded credentials

The database seed creates these accounts:

- `superuser` / `superuser123!`
- `electronics_staff` / `electronics123!`
- `books_staff` / `books123!`

See `submission.json` for the machine-readable credential payload.

## Local development

If you want to run against SQLite locally, keep `DATABASE_ENGINE=django.db.backends.sqlite3` in your environment and run:

```bash
python manage.py migrate
python manage.py seed_inventory
python manage.py runserver
```

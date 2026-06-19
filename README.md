# Django Admin Inventory System

This project turns the Django admin into a complete internal inventory application. It demonstrates:

- Product list customization with computed stock-status badges
- An atomic admin action (`mark_clearance`) that updates prices and creates `StockAudit` logs
- A custom admin dashboard at `/admin/inventory/dashboard/` with efficient DB aggregation
- Row-level edit permissions based on the `Profile.managed_category` field
- Read-only `StockAudit` inlines on product change pages
- Docker Compose setup (Postgres) with automatic seeding on startup

---

Quickstart (Docker)

1. Copy `.env.example` to `.env` and edit values if needed.
2. Build and start the stack in detached mode:

```powershell
docker compose up --build -d
```

3. Check services and health:

```powershell
docker compose ps
docker compose logs --tail 100 web
```

4. Visit the admin: `http://localhost:8000/admin/`

Seeded credentials (for demo/video)

- Superuser (full access)
	- Username: `superuser`
	- Password: `superuser123!`

- Electronics staff (can view/edit Electronics only)
	- Username: `electronics_staff`
	- Password: `electronics123!`

- Books staff (can view/edit Books only)
	- Username: `books_staff`
	- Password: `books123!`

The machine-readable credentials are in `submission.json`.

If you want a fourth account (read-only viewer) for the video, tell me and I'll add it to the seed.

Local development (optional)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_inventory
python manage.py runserver
```

Verifications and useful commands

- Re-run seeding (idempotent):

```powershell
docker compose exec web python manage.py seed_inventory
```

- Run inventory tests:

```powershell
docker compose exec web python manage.py test inventory
```

- Check seeded counts quickly:

```powershell
docker compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; from inventory.models import Product,Profile,StockAudit; User=get_user_model(); print('users',User.objects.count()); print('products',Product.objects.count()); print('profiles',Profile.objects.count()); print('audits',StockAudit.objects.count())"
```

UI notes (what changed)

- Custom admin theme and persistent theme toggle (Auto/Light/Dark) implemented via `inventory/static/admin-custom/*` and the `templates/admin/base_site.html` override.
- Stock status badges use CSS classes and consistent styling; inline audits are read-only.

Recording checklist (what to show in your video)

1. Project overview & architecture (1–2 minutes)
2. `docker compose up --build -d` and `docker compose ps` (show health)
3. Log in as `superuser` — demo full admin, run `mark_clearance`, show `StockAudit` entries
4. Log in as `electronics_staff` — show Electronics product edit success and Books product forbidden
5. Log in as `books_staff` — mirror the above for Books
6. Visit `/admin/inventory/dashboard/` to show aggregated total value and low-stock list
7. Open a product with audit logs and show the inline is read-only
8. Show `python manage.py test inventory` or seed command output as evidence of automated checks
9. Wrap up: how to run locally and where to find credentials (`submission.json`)

---

If you want this README shortened, expanded with screenshots, or to include the exact commands you used to record the demo (terminal transcripts), tell me which format you prefer and I'll adjust it.

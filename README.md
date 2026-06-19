# Inventory Admin — Implementation Summary

This project implements an internal inventory product inside the Django admin. The README below is concise and focused on implementation and verification.

Project description
-------------------

An admin-first inventory management system that demonstrates: custom ModelAdmin behavior, custom admin views, atomic admin actions with audit logging, row-level (object) permissions, and simple theming — all packaged with Docker Compose and an idempotent seed command for demos.

Tech stack
----------

- Python 3.11+ / Django 5
- PostgreSQL (docker: postgres:16-alpine)
- Gunicorn, Docker, Docker Compose

Folder structure (important files)
---------------------------------

- `config/` — project settings and `urls.py`
- `inventory/`
	- `models.py` — `Product`, `StockAudit`, `Profile`
	- `admin.py` — `ProductAdmin`, admin action, dashboard view, inlines
	- `management/commands/seed_inventory.py` — seeding script
	- `templates/admin/inventory/dashboard.html` — dashboard template
	- `static/admin-custom/` — CSS, logo, theme JS
- `templates/admin/base_site.html` — admin branding override
- `docker-compose.yml`, `Dockerfile`, `submission.json`

Docker quick steps
------------------

1. (Optional) Copy env file:

```powershell
copy .env.example .env
```

2. Build and start services:

```powershell
docker compose up --build -d
```

3. Confirm services and health:

```powershell
docker compose ps
docker compose logs --tail 200 web
```

4. Re-seed (idempotent):

```powershell
docker compose exec web python manage.py seed_inventory
```

5. Collect static if needed:

```powershell
docker compose exec web python manage.py collectstatic --noinput
```

Implementation summary
----------------------

- Models: `Product` (name, sku, price, stock, category), `StockAudit`, `Profile` (user → managed_category).
- Admin features:
	- `ProductAdmin` with `list_display` (name, SKU, price, stock, category, stock status badge), `list_filter`, `search_fields`, `list_editable` for `stock`.
	- `StockAuditInline` is read-only and optimized via `select_related`.
	- `mark_clearance` admin action: transactional, row-locked (`select_for_update()`), halves price and writes `StockAudit` records.
	- Dashboard registered via `ProductAdmin.get_urls()` at `/admin/inventory/dashboard/`; uses DB-side aggregation (`ExpressionWrapper` + `Sum`).
- Permissions: `ProductAdmin.has_change_permission()` enforces row-level editing by comparing `obj.category` to `request.user.profile.managed_category`; superusers bypass.
- UI: small theme toggle + custom CSS under `inventory/static/admin-custom/` and `templates/admin/base_site.html` override.

Verification & useful commands
-----------------------------

- Run tests:

```powershell
docker compose exec web python manage.py test inventory
```

- Quick counts (users/products/profiles/audits):

```powershell
docker compose exec web python manage.py shell -c "from django.contrib.auth import get_user_model; from inventory.models import Product,Profile,StockAudit; User=get_user_model(); print('users',User.objects.count()); print('products',Product.objects.count()); print('profiles',Profile.objects.count()); print('audits',StockAudit.objects.count())"
```

Seeded demo credentials
-----------------------

- `superuser` / `superuser123!`
- `electronics_staff` / `electronics123!`
- `books_staff` / `books123!`


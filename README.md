# SneakPick

A Django e-commerce web application for browsing and buying sneakers.

## Author

Rakib Rayhan — rakib.rayhan@northsouth.edu

## Features

- **Products** — catalog with product detail pages and images
- **Users** — signup, login/logout, profile
- **Cart** — add/remove items, view cart
- **Orders** — order placement and tracking, with estimated delivery time and shipping charge
- **Shipping** — configurable shipping methods and charges
- **Payment** — checkout flow, saved bank account details
- **Promotions** — promotional offers
- **Reviews** — product ratings and reviews (under `users`)

## Tech stack

- Django 5.1.3
- SQLite (default local database)
- Pillow (image handling)

Full dependency versions are in `requirements.txt`.

## Project structure

```
.
├── shoes/           # project settings, root URL config
├── home/            # landing page
├── products/        # product catalog
├── users/           # auth, profiles, reviews
├── cart/            # shopping cart
├── orders/          # order placement & tracking
├── shipping/        # shipping methods
├── payment/         # checkout & payment
├── promotions/      # promotional offers
├── templates/        # shared base template
├── static/           # shared CSS
├── media/products/   # product images
└── docs/              # Sphinx documentation source
```

Each app follows standard Django conventions: `models.py`, `views.py`, `urls.py`,
`templates/`, and a `migrations/` folder with the full migration history.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit `http://127.0.0.1:8000/`, and `http://127.0.0.1:8000/admin/` for the
Django admin.

## Notes

- `db.sqlite3` is not committed — running `migrate` above builds a fresh,
  empty database. Load your own product data via the admin panel, or a
  fixture if one is added later.
- `SECRET_KEY` in `shoes/settings.py` is a Django dev placeholder and
  `DEBUG = True`. Both are fine for local/coursework use but should be
  replaced with environment variables before any real deployment.
- Product images under `media/products/` are included so the storefront
  renders with real content out of the box.

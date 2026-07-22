# MC Rentals

*Find. Buy. Rent. Invest.*

## The Problem

Renting out houses and rooms informally usually means juggling WhatsApp statuses, Facebook marketplace posts, and word of mouth. Tenants never get a straight answer on the things that actually decide whether a place is livable — is there running water, mains electricity, backup power for load-shedding, a full description, real photos, an actual price? They have to message an agent just to find out basics, and half the "available" listings they hear about turn out to be already rented.

On the other side, whoever manages the properties has no single place to track which houses are occupied, who's living in each one, when their lease started or ends, and what they're paying — that all lives in someone's head or a notebook.

## The Solution

**MC Rentals** is a self-hosted rental listing site with two sides:

- **Public site** — tenants browse available houses/rooms with full descriptions, pricing, photos, bedroom/bathroom counts, and a clear amenities section (water, electricity, backup power, Wi-Fi, security, parking, furnished). Every listing has one-tap **WhatsApp** and **Call** buttons that go straight to the property manager — no sign-up, no middleman.
- **Admin panel** — the property manager (or their staff, multiple admin accounts are supported) can add or remove listings, upload photos, toggle a house between **Available** and **Occupied** with one click, and keep a running record of occupants per property: name, contact, move-in date, lease end date, and agreed rent.

Everything is built to feel like a real product, not a template — a consistent navy/gold brand, scroll and hover animations, dark/light mode, and a fully responsive layout from phone to desktop.

---

## Tech Stack

- **Backend:** Flask (Python), SQLAlchemy ORM, Flask-Login (multi-admin auth), Flask-WTF (forms + CSRF protection)
- **Database:** SQLite (single file, zero setup)
- **Frontend:** Server-rendered Jinja2 templates, hand-written CSS (design tokens, no framework), vanilla JavaScript (scroll-reveal, lightbox gallery, mobile nav, dark-mode toggle)
- **Images:** Pillow, for resizing/normalizing uploaded photos on save

No Node build step, no external services required to run locally.

## Project Structure

```
mc-rentals/
├── app.py                   # entry point (flask run / python app.py)
├── config.py                # app config, env vars, secret key handling
├── create_admin.py          # CLI to bootstrap the first admin account
├── requirements.txt
├── instance/                # SQLite database file lives here (gitignored)
└── app/
    ├── __init__.py           # app factory
    ├── extensions.py         # db, login manager, CSRF
    ├── models.py             # House, HouseImage, Occupant, Admin, Setting
    ├── forms.py              # WTForms for listings, occupants, settings, auth
    ├── utils.py               # image saving, WhatsApp/tel link helpers
    ├── template_helpers.py    # Jinja filters/context (currency, contact numbers)
    ├── routes/
    │   ├── public.py          # home, listings, house detail
    │   ├── auth.py             # login/logout
    │   └── admin.py            # listings/occupants/settings/admin-user CRUD
    ├── templates/              # Jinja2 templates (public + admin)
    └── static/
        ├── css/                 # tokens.css + one file per page/area
        ├── js/                  # main.js, gallery.js, admin.js
        ├── images/               # logo, icon, hero photo
        └── uploads/              # admin-uploaded listing photos (gitignored)
```

## Getting Started

### 1. Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Set a secret key (recommended)

```bash
set SECRET_KEY=replace-with-a-long-random-string        # Windows (cmd)
$env:SECRET_KEY="replace-with-a-long-random-string"      # PowerShell
```

If you skip this, the app still runs but falls back to an insecure default key with a warning — fine for local testing, not for anything public-facing.

### 3. Create your first admin account

```bash
python create_admin.py <username> <password>
```

You can add more admin accounts later from inside the admin panel (**Admin Users** page).

### 4. Run the app

```bash
python app.py
```

Visit `http://127.0.0.1:5000` for the public site, and `http://127.0.0.1:5000/admin/login` to sign in.

### 5. Configure contact details

Once logged in, go to **Contact Settings** in the admin sidebar and set the WhatsApp number, phone number, and currency symbol used across the site — these all start blank/default until you set them.

## Core Features

**For tenants (public site)**
- Home page with featured available listings and quick stats
- Filterable listings page (type, location, price range, bedrooms, availability, keyword search)
- House detail page: photo gallery with lightbox, full description, amenities/utilities, availability badge
- Direct WhatsApp (pre-filled message) and Call buttons on every listing

**For the property manager (admin panel)**
- Add / edit / delete listings, with drag-and-drop multi-photo upload
- One-click Available ⇄ Occupied toggle
- Occupant records per property (name, contact, move-in/lease-end dates, rent, notes) — deleting the last occupant automatically reverts the listing to Available
- Multiple admin accounts with independent logins
- Site-wide contact number and currency settings

## Notes on Security

- CSRF protection is enabled globally (Flask-WTF `CSRFProtect`) across every form and state-changing action.
- Passwords are hashed with Werkzeug's `generate_password_hash` — never stored in plain text.
- Session cookies are `HttpOnly` and `SameSite=Lax` by default; set `FORCE_SECURE_COOKIES=true` once you're serving over HTTPS.
- Uploaded images are validated by actually opening them with Pillow, not just checking the file extension.

## License

Private project for MC Rentals. Not licensed for redistribution.

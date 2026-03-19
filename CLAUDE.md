# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Run development server
python manage.py runserver

# Database migrations (board app uses SQLite default)
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test
python manage.py test board   # single app
python manage.py test app     # single app

# Create superuser for admin
python manage.py createsuperuser

# Inspect existing DB schema (used to generate app/models.py)
python manage.py inspectdb --database=mysql_db
```

## Architecture

This is a Django 6.0.3 learning project with two apps and a **dual-database setup**:

### Dual-Database Routing

- `default` — SQLite (`db.sqlite3`), used by the `board` app
- `mysql_db` — MySQL (`bookmark` database on `127.0.0.1:3306`), used by the `app` app
- `mysite/routers.py` contains `AppRouter` which routes all `app` models to `mysql_db` and everything else to `default`

When running migrations, specify the database:
```bash
python manage.py migrate --database=default       # board app
python manage.py migrate --database=mysql_db      # app app
```

### Apps

**`app/`** — Bookmark manager backed by MySQL
- Models: `Bookmarks`, `Tags`, `BookmarkTags` — all with `managed = False` (pre-existing tables, not Django-managed)
- Views: `index`, `test` (DB connection check), `picrotate` (image rotator), `get_bookmarks` (JSON API), `bookmark` (search)
- URL namespace: `app`, mounted at `/app/`

**`board/`** — Simple message guestbook backed by SQLite
- Model: `Message` (content + timestamp), Django-managed with migrations in `board/migrations/`
- View: `index` handles both GET (list) and POST (create), uses PRG pattern (redirect after POST)
- URL namespace: `board`, mounted at `/board/`

### URL Structure

```
/admin/          → Django admin
/app/            → app:index
/app/test/       → app:test
/app/picrotate/  → app:picrotate
/app/get-bookmarks/ → app:get_bookmarks (JSON)
/app/bookmark    → app:bookmark (search, GET/POST)
/board/          → board:index (GET/POST)
```

### Key Patterns

- `app` models use `managed = False` — do not run `makemigrations` for the `app` app; the MySQL schema is managed externally
- Templates live in `<app>/templates/<app>/` (app-namespaced)
- Static files live in `<app>/static/<app>/`

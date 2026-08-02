# Films TODO

A Django watchlist for movies: search via [Kinopoisk Unofficial API](https://kinopoiskapiunofficial.tech/documentation/api/), save titles to "watch later", and browse details (cast, ratings, where to watch).

## Stack

- **Backend**: Django 6.0 + Django REST Framework
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **Container Runtime**: Docker Compose v2
- **Language**: Python 3.12

## Features

- Search films by title and add them to your watchlist
- Movie detail page with Kinopoisk / IMDb ratings, cast, premieres, and streaming links
- User authentication and per-user watchlist management
- Django admin at `/admin/`
- Structured business logic via services layer
- Full Docker Compose stack: Django, PostgreSQL, Redis, nginx

## Requirements

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose v2
- API key from [kinopoiskapiunofficial.tech](https://kinopoiskapiunofficial.tech) (register and copy your token)

## Quick Start

### 1. Clone the repository

```sh
git clone https://github.com/AlexanderVerner/films-todo.git
cd films-todo
```

### 2. Create `.env` from the example

Copy the template and fill in your secrets (API token, database password, admin credentials):

```sh
cp .env.example .env
```

Edit `.env` and add your actual values:

```env
# Required: Kinopoisk API token (get from https://kinopoiskapiunofficial.tech)
KINOPOISK_TOKEN=your-api-key-here

# Database password (matches POSTGRES_PASSWORD in .env)
POSTGRES_PASSWORD=your-secure-db-password

# Optional: Admin user created during first migration
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-admin-password
ADMIN_EMAIL=admin@localhost.local
```

**Important**: 
- `.env` is in `.gitignore` — never commit it
- Always use strong passwords for `POSTGRES_PASSWORD` in production
- `SECRET_KEY` and `DEBUG` should be set per environment (defaults provided for local development only)

See `.env.example` for all available configuration variables.

### 3. Install frontend vendor assets (first time only)

Static libraries (jQuery, Bootstrap, etc.) live under `_project_/static/todo/lib/` and are not committed. Install them once:

```sh
cd _project_/static/todo
docker run --rm -v "$PWD:/work" -w /work node:20-alpine sh -c \
  "apk add --no-cache git curl && npm i -g bower && bower install --allow-root && \
   curl -fsSL -o lib/smoothscroll.js \
   https://raw.githubusercontent.com/galambalazs/smoothscroll-for-websites/master/SmoothScroll.js"
cd ../../..
```

Without this step the site may show an endless "Loading…" overlay because jQuery fails to load.

### 4. Run the stack

```sh
docker compose up --build -d
```

On startup, the `web` container runs migrations and starts the dev server.

| Service   | URL | Purpose |
|-----------|-----|---------|
| App (dev) | http://localhost:8000 | Django dev server |
| Admin     | http://localhost:8000/admin/ | Django admin panel |
| nginx     | http://localhost:80 | Reverse proxy / static files |
| PostgreSQL | localhost:5432 | Database (internal only) |
| Redis | localhost:6379 | Cache (internal only) |

Log in with credentials from `ADMIN_USERNAME` / `ADMIN_PASSWORD` in your `.env`.

### 5. Useful commands

```sh
# View running services
docker compose ps

# Stream web container logs
docker compose logs -f web

# Open Django shell
docker compose exec web python manage.py shell

# Stop all services
docker compose down
```

## Running Tests

### Using pytest (recommended)

The primary way to run tests is with pytest:

```sh
# All tests with coverage
docker compose exec web pytest

# Specific app
docker compose exec web pytest todo/

# Specific test file
docker compose exec web pytest todo/tests/test_services.py

# Specific test class or function
docker compose exec web pytest todo/tests/test_services.py::FilmsServiceTests::test_search
```

Coverage output is generated in HTML format; view the report after running tests.

**Coverage requirements**:
- `todo/services/`: ≥ 80%
- `todo/api/`: ≥ 50%

### Using run_tests.py (alternative)

Inside the running `web` container, you can also use the custom test runner:

```sh
# All tests
docker compose exec web python run_tests.py todo

# Single test module
docker compose exec web python run_tests.py todo.tests.test_view
```

### In PyCharm IDE

Configure Django settings as follows:
- **Django project root**: `.`
- **Django settings module**: `_project_.settings`
- **Test runner**: pytest or unittest (Django)

For running app-specific tests, use `_project_.run_tests_settings` as the settings module.

## Security

### Environment Variables

**Never commit `.env`** — it contains secrets. The file is in `.gitignore` for this reason.

Sensitive variables:
- `SECRET_KEY`: Used for session encryption and CSRF tokens. Must be a long, random string in production.
- `DEBUG`: Set to `false` in production. When `true`, Django exposes detailed error pages.
- `POSTGRES_PASSWORD`: Database password. Use a strong, unique password.
- `KINOPOISK_TOKEN`: API token. Do not share or commit.

Each environment (local, staging, production) must have its own `.env` file with appropriate values.

### Database Security

- PostgreSQL requires a password for the `film_todo` user (set via `POSTGRES_PASSWORD` in `.env`)
- In production, enable `POSTGRES_USE_TLS=true` to encrypt database connections
- Use strong passwords (20+ characters with mixed case, numbers, symbols)

## Architecture

```
Views (Django views + REST endpoints)
  ↓
Services Layer (business logic)
  ├─ FilmsService (search, fetch film details)
  └─ NoteService (create, read, update, delete user watchlist)
  ↓
Kinopoisk API Client + Models + Cache (Redis)
  ↓
Database (PostgreSQL)
```

### Layers

1. **Views** (`todo/views.py`): HTTP request handlers, authentication checks, response formatting
2. **Services** (`todo/services/`):
   - `FilmsService`: Searches films via Kinopoisk API, handles errors, logs operations
   - `NoteService`: Manages user notes/watchlist, validates ownership, optimizes DB queries
3. **API Client** (`todo/kinopoisk_api.py`): Low-level integration with Kinopoisk Unofficial API
4. **Models** (`todo/models.py`): ORM definitions for `Movie`, `Note`, and related data
5. **Cache** (Redis): Caches Kinopoisk API responses to reduce external API calls

### Authentication & Authorization

- User authentication via Django's built-in system (session-based)
- Each note is tied to a specific user; users can only view/edit/delete their own notes
- Admin users can access the Django admin panel at `/admin/`

## Configuration Reference

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `SECRET_KEY` | `dev-insecure-secret-key-only-for-local-development` | ✓ | Session/CSRF encryption key (set long random string in production) |
| `DEBUG` | `true` | ✓ | Enable detailed error pages in development; **must be `false` in production** |
| `KINOPOISK_TOKEN` | (empty) | ✓ | API key for Kinopoisk Unofficial API |
| `KINOPOISK_API_URL` | `https://kinopoiskapiunofficial.tech` | | Base URL for Kinopoisk API |
| `MAX_COUNT_MOVIE_PER_REQUEST` | `15` | | Maximum search results per API request |
| `ALLOWED_HOSTS` | `["todo.film", "localhost"]` | | JSON array of allowed host names |
| `ADMIN_USERNAME` | (empty) | | Superuser username created on first migration (if set) |
| `ADMIN_PASSWORD` | (empty) | | Superuser password created on first migration (if set) |
| `ADMIN_EMAIL` | (empty) | | Superuser email created on first migration (if set) |
| `POSTGRES_HOST` | `postgresdb` | | Database host (internal Docker network) |
| `POSTGRES_USER` | `film_todo` | | Database user |
| `POSTGRES_PASSWORD` | `change-me-in-local-env` | ✓ | Database password (must be changed) |
| `POSTGRES_DATABASE_NAME` | `film_todo` | | Database name |
| `POSTGRES_USE_TLS` | `false` | | Enable TLS for database connections |
| `TEST_POSTGRES_DATABASE_NAME` | `film_todo_test` | | Separate database name for tests |

## API Endpoints

### Films

- `GET /api/films/search/?q=<query>&limit=<int>` — Search films by title
- `GET /api/films/<id>/` — Get detailed film information

### Notes (User Watchlist)

- `GET /api/notes/` — List user's watchlist
- `POST /api/notes/` — Add a film to watchlist
- `GET /api/notes/<id>/` — Get note details
- `DELETE /api/notes/<id>/` — Remove from watchlist

### Admin

- `GET/POST /admin/` — Django admin panel (authenticated superusers only)

## Project Layout

```
films-todo/
├── _project_/              # Django project configuration
│   ├── settings.py         # Main Django settings
│   ├── urls.py             # Root URL router
│   ├── templates/todo/     # HTML templates
│   ├── static/todo/        # CSS, JS, vendor libs (Bower)
│   └── wsgi.py             # WSGI entry point
├── _local_deploy/          # Docker environment & nginx
│   ├── common.env          # Shared environment defaults
│   └── nginx.conf          # Nginx configuration
├── todo/                   # Main Django app
│   ├── views.py            # HTTP request handlers
│   ├── models.py           # ORM models (Movie, Note)
│   ├── forms.py            # Django forms
│   ├── admin.py            # Django admin configuration
│   ├── urls.py             # App URL router
│   ├── serializers.py      # DRF serializers
│   ├── kinopoisk_api.py    # Kinopoisk API integration
│   ├── services/           # Business logic layer
│   │   ├── films.py        # FilmsService
│   │   └── notes.py        # NoteService
│   ├── templatetags/       # Custom template filters
│   ├── migrations/         # Database migrations
│   └── tests/              # Test suite
├── docker-compose.yml      # Container orchestration
├── Dockerfile              # Django container definition
├── manage.py               # Django management CLI
├── run_tests.py            # Custom test runner
├── requirements.txt        # Python dependencies
├── .env                    # Local secrets (git-ignored)
├── .env.example            # Template for .env
└── .gitignore              # Git exclusion rules
```

## License

See repository history and authors for licensing terms if applicable.

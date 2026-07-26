# Films TODO

A Django watchlist for movies: search via [Kinopoisk Unofficial API](https://kinopoiskapiunofficial.tech/documentation/api/), save titles to “watch later”, and browse details (cast, ratings, where to watch).

## Features

- Search films by title and add them to your list
- Movie detail page with Kinopoisk / IMDb ratings, cast, premieres, and streaming links
- Django admin at `/admin/`
- Docker Compose stack: Django, PostgreSQL, nginx

## Requirements

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose v2
- API key from [kinopoiskapiunofficial.tech](https://kinopoiskapiunofficial.tech) (register and copy your token)

## Quick start

### 1. Clone the repository

```sh
git clone https://github.com/AlexanderVerner/films-todo.git
cd films-todo
```

### 2. Create `.env`

The app loads `_local_deploy/common.env` first, then **`.env`** (values in `.env` override shared defaults).  
Create `.env` in the project root — it is listed in `.gitignore` and is the right place for secrets.

```sh
touch .env
```

Minimal example:

```env
# Kinopoisk Unofficial API (required for search and film details)
KINOPOISK_TOKEN=your-api-key-here

# Optional: used when running migrations (todo.0002_generate_superuser)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin
ADMIN_EMAIL=admin@localhost
```

`KINOPOISK_API_URL` defaults to `https://kinopoiskapiunofficial.tech` in `_local_deploy/common.env`; override it in `.env` only if needed.

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

Without this step the site may show an endless “Loading…” overlay because jQuery fails to load.

### 4. Run the stack

```sh
docker compose up --build -d
```

On startup the `web` container runs migrations and starts the dev server.

| Service   | URL |
|-----------|-----|
| App (dev) | http://localhost:8000 |
| Admin     | http://localhost:8000/admin/ |
| nginx     | http://localhost:80 |

Use the admin credentials from `ADMIN_*` in `.env` (created on first migrate if set).

### Useful commands

```sh
docker compose ps
docker compose logs -f web
docker compose down
```

## Configuration reference

| Variable | Description |
|----------|-------------|
| `KINOPOISK_TOKEN` | API key for Kinopoisk Unofficial API (**required**) |
| `KINOPOISK_API_URL` | API base URL (default: `https://kinopoiskapiunofficial.tech`) |
| `MAX_COUNT_MOVIE_PER_REQUEST` | Max search results per request (default: `15`) |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` / `ADMIN_EMAIL` | Superuser created by migration `0002_generate_superuser` |
| `ALLOWED_HOSTS` | JSON array of hosts (see `_local_deploy/common.env`) |
| `POSTGRES_*` | Database settings for Docker (see `_local_deploy/common.env`) |

## Running tests

Inside the running `web` container:

```sh
# All tests
docker compose exec web ./run_tests_locally.py

# App
docker compose exec web ./run_tests_locally.py todo

# Module or single test
docker compose exec web ./run_tests_locally.py todo.tests.test_view
docker compose exec web ./run_tests_locally.py todo.tests.test_view.IndexViewTests.test_get_index_view
```

### PyCharm

Use custom Django settings: `_project_/run_tests_settings.py`.

## Project layout

```
films-todo/
├── _project_/              # Django project (settings, templates, static)
│   ├── templates/todo/     # App HTML templates
│   └── static/todo/        # CSS/JS; vendor libs in lib/ (Bower)
├── _local_deploy/          # Docker env defaults and nginx config
├── todo/                   # Main app (models, views, Kinopoisk client)
│   ├── kinopoisk_api.py    # Kinopoisk Unofficial API integration
│   └── templatetags/       # Template filters (ratings, cast, watch links)
├── docker-compose.yml
├── Dockerfile
├── manage.py
└── .env                    # Local secrets (create yourself, not in git)
```

## License

See repository history and authors for licensing terms if applicable.

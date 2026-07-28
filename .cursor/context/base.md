# Контекст проекта

## О проекте
**Название:** films-todo
**Цель:** REST API сервис для хранения фильмов и вытягивания информации о фильмах по Kinopoisk API

## Стек
- Backend: Python 3.12.3, Django framework
- БД: PostgreSQL, Django ORM
- Кэш: Redis
- Тестирование: pytest + плагин pytest-django, mock
- Конфиг: pipenv, pydantic-settings
- Контейнеризация: Docker, docker-compose
- Сервер: nginx

## Архитектура

```
films-todo/
├── _project_/                     # Django project: глобальная конфигурация
│   ├── settings.py                # Apps, middleware, БД, env, static/templates
│   ├── urls.py                    # Корневая маршрутизация
│   ├── asgi.py / wsgi.py          # Серверные entrypoints
│   ├── templates/		           # Presentation layer
│   └── static/
│
├── todo/                          # Единственное доменное Django-приложение
│   ├── models.py                  # Описание модели данных
│   ├── views.py                   # Контроллер вью
│   ├── urls.py                    # Маршруты приложения
│   ├── forms.py                   # Формы
│   ├── kinopoisk_api.py           # Методы приложения
│   ├── migrations/                # История схемы БД
│   └── tests/
│
├── _local_deploy/
│   ├── common.env                 # Ключи-переменные для параметров
│   └── nginx.conf                 # Reverse proxy, SSL и static - конфиг для nginx
│
├── Dockerfile
├── docker-compose.yml             # Django + PostgreSQL + nginx
├── Pipfile / Pipfile.lock
├── run_tests.py
├── run_tests_locally.py
├── manage.py                      # Входная точка приложения
├── README.md                      # Ридми для приложения в гит
└── .env                           # Локальные секреты, не отслеживается Git
```

## Соглашения
- Git: Conventional Commits (feat/fix/refactor/docs/test/chore)
- Ошибки: всегда raise SpecificError("context") from err (сохранять traceback), не игнорировать (никаких пустых except: pass)
- Логирование: structured logging, structlog или стандартный logging с JSON-форматтером (никаких print() в бизнес-логике)
- Интерфейсы: typing.Protocol (structural subtyping) или ABC, определять в модуле потребителя (не в repository)
- Тесты: pytest + нативный assert, моки через unittest.mock (часто через плагин pytest-mock)
- Минимум coverage: 80% для services/, 50% для api/ (через pytest-cov)

## Исключения (не трогать)
- migrations/ — SQL миграции, только вручную
- .env — секреты, не коммитить

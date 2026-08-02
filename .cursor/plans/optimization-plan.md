# План оптимизации
Создан: 2026-07-29
Завершён: 2026-08-02

## Очередь
(все задачи выполнены)

## Выполнено
- [x] task-001 — Исправить makemigrations для несуществующего app `tests` (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-002 — Заменить exec в run_tests_settings на importlib (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-003 — Вынести SECRET_KEY и DEBUG в переменные окружения (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-004 — Убрать захардкоженный пароль PostgreSQL из docker-compose (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-005 — Закрыть прямой доступ к Django на порту 8000 (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-006 — Изолировать тестовую БД от рабочей (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-007 — Обработка сетевых ошибок и JSONDecode в kinopoisk_get (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-008 — Логировать и не маскировать сбои Kinopoisk в fetch_* (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-009 — Корректные HTTP-коды при недоступности Kinopoisk во views (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-010 — Перевести сохранение заметки с GET на POST (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-011 — Валидация URL в format_watchability против javascript: XSS (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-012 — Исправить вложенные формы и разметку detail.html (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-013 — Починить подсчёт строк в analyze-project-structure.sh (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-014 — Убрать eval из test-framework.sh (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-015 — JSONField default=list в models и миграция (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-016 — Подключить nginx.conf вместо неиспользуемого .template (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-017 — Исправить CORS, SSL и маршрутизацию proxy в nginx (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-018 — Убрать нерабочий constance.backends.database из INSTALLED_APPS (03-fix-simple-bug) ✅ 2026-08-02
- [x] task-019 — Настроить structured LOGGING в settings (05-refactor) ✅ 2026-08-02
- [x] task-020 — Общий хелпер декодирования ответов Kinopoisk (05-refactor) ✅ 2026-08-02
- [x] task-021 — select_related и очистка get_note_list (05-refactor) ✅ 2026-08-02
- [x] task-022 — Вынести маппинг API→Movie из SaveView (05-refactor) ✅ 2026-08-02
- [x] task-023 — Добавить pytest и dev-зависимости в Pipfile (05-refactor) ✅ 2026-08-02
- [x] task-024 — Устранить дублирующиеся тесты SaveView (05-refactor) ✅ 2026-08-02
- [x] task-025 — Единый базовый модуль настроек prod/test (05b-refactor-complex) ✅ 2026-08-02
- [x] task-026 — Нормализовать контракт search_films / fetch_film_details (05b-refactor-complex) ✅ 2026-08-02
- [x] task-027 — Слой services для заметок и интеграции Kinopoisk (04-create-architecture) ✅ 2026-08-02
- [x] task-028 — Аутентификация и проверка владельца заметок (IDOR) (04-create-architecture) ✅ 2026-08-02
- [x] task-029 — Подключить Redis CACHES для ответов Kinopoisk (05-refactor) ✅ 2026-08-02
- [x] task-030 — Unit-тесты ошибок и границ kinopoisk_api (06-write-unit-tests) ✅ 2026-08-02
- [x] task-031 — Unit-тесты views: Detail, Delete, POST preview, доступ (06-write-unit-tests) ✅ 2026-08-02
- [x] task-032 — Обновить README: стек, тесты, docker, секреты (09-update-readme) ✅ 2026-08-02

## Итого
**Всего задач: 32/32 ✅**
**Статус: ЗАВЕРШЕНО**
**Дата завершения: 2026-08-02**
**Бюджет: ~$2.95 (использовано)**

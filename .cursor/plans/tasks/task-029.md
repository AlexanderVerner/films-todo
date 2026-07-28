# Задача 029: Подключить Redis CACHES для ответов Kinopoisk

## Проблема
Redis в стеке, но не настроен — 4 последовательных HTTP на каждую деталь.

## Файл
`_project_/settings.py`

## Функция
`CACHES` (~1)

## Решение
Добавить сервис redis в compose, `CACHES` с django-redis; кэшировать build_film_detail/search по ключу film_id.

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
refactor: cache kinopoisk responses in redis

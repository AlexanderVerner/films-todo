# Задача 019: Настроить structured LOGGING в settings

## Проблема
Нет секции LOGGING — сбои Kinopoisk и views не фиксируются (требование base.md).

## Файл
`_project_/settings.py`

## Функция
`(модуль)` (~1)

## Решение
Добавить `LOGGING` с JSON-форматтером или structlog-совместимой конфигурацией; логгеры `todo` и `django.request`.

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
refactor: add structured logging configuration

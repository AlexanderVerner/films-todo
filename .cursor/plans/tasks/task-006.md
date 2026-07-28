# Задача 006: Изолировать тестовую БД от рабочей

## Проблема
Тестовые настройки используют те же `POSTGRES_*`, что и прод — риск порчи данных при прогоне тестов.

## Файл
`todo/tests/settings.py`

## Функция
`(модуль)` (~66)

## Решение
Задать отдельное имя БД (суффикс `_test`), sqlite для CI или env `TEST_DATABASE_URL`; не переиспользовать рабочую БД по умолчанию.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: isolate test database configuration

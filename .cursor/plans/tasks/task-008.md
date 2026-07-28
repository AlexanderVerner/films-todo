# Задача 008: Логировать и не маскировать сбои Kinopoisk в fetch_*

## Проблема
При статусе ≠200 функции возвращают `{}`/`[]` без логов — 401/429 выглядят как пустые данные фильма.

## Файл
`todo/kinopoisk_api.py`

## Функция
`fetch_film_staff / fetch_film_distributions / fetch_film_external_sources` (~70)

## Решение
Единая проверка статуса: лог status/body (без ключа), для клиентских ошибок — явный результат или исключение, не пустая заглушка без следа.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: stop silently swallowing kinopoisk api errors

# Задача 030: Unit-тесты ошибок и границ kinopoisk_api

## Проблема
Покрыты только happy-path; критичные ветки без тестов.

## Файл
`todo/tests/test_kinopoisk_api.py`

## Функция
`KinopoiskApiMappingTests` (~16)

## Решение
Тесты на ≠200, JSONDecode, limit, parse_age_rating, staff_by_profession; pytest + mock kinopoisk_get.

## Промпт
`06-write-unit-tests.txt`

## Модель
Haiku С thinking

## Commit
test: cover kinopoisk api error paths

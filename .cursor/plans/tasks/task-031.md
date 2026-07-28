# Задача 031: Unit-тесты views: Detail, Delete, POST preview, доступ

## Проблема
Не покрыты Delete, Detail, ошибка API, POST preview; IDOR не ловится.

## Файл
`todo/tests/test_view.py`

## Функция
`IndexViewTests / PreViewTests` (~34)

## Решение
Тесты после task-028: чужая заметка 404/403, delete, preview POST с mock API.

## Промпт
`06-write-unit-tests.txt`

## Модель
Haiku С thinking

## Commit
test: expand view coverage and access control

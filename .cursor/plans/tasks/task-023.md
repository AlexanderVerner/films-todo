# Задача 023: Добавить pytest и dev-зависимости в Pipfile

## Проблема
В base.md заявлен pytest, но `[dev-packages]` пуст — coverage и стиль тестов не выровнять.

## Файл
`Pipfile`

## Функция
`(модуль)` (~1)

## Решение
Добавить pytest, pytest-django, pytest-mock, pytest-cov; выровнять python_version с 3.12 при необходимости отдельной задачей.

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
refactor: add pytest dev dependencies

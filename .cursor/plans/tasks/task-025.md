# Задача 025: Единый базовый модуль настроек prod/test

## Проблема
~95% дублирования между `_project_/settings.py` и `todo/tests/settings.py`.

## Файл
`_project_/settings.py`

## Функция
`(модуль)` (~1)

## Решение
Вынести общее в `_project/settings_base.py`, prod и test импортируют и переопределяют только отличия.

## Промпт
`05b-refactor-complex.txt`

## Модель
Sonnet С thinking (medium)

## Commit
refactor: deduplicate django settings modules

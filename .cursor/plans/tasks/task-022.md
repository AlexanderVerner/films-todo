# Задача 022: Вынести маппинг API→Movie из SaveView

## Проблема
22-строчный `defaults={...}` во view смешивает HTTP и доменную логику.

## Файл
`todo/views.py`

## Функция
`SaveView` (~66)

## Решение
Функция `movie_defaults_from_detail(detail: dict) -> dict` в отдельном модуле (подготовка к services/).

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
refactor: extract movie mapping from save view

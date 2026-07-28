# Задача 011: Валидация URL в format_watchability против javascript: XSS

## Проблема
Произвольный `href` из API попадает в `mark_safe` — stored XSS через поле watchability.

## Файл
`todo/templatetags/todo_extras.py`

## Функция
`format_watchability` (~33)

## Решение
Разрешать только `http`/`https` схемы (urllib.parse); иначе выводить текст без ссылки или пустую строку.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: validate watchability urls before mark_safe

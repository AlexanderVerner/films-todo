# Задача 010: Перевести сохранение заметки с GET на POST

## Проблема
SaveView изменяет БД по GET — неидемпотентно, уязвимо к CSRF/префетчу.

## Файл
`todo/views.py`

## Функция
`SaveView.get` (~66)

## Решение
Реализовать `post`, обновить `todo/urls.py`, шаблоны и тесты на POST с CSRF; GET оставить редиректом или 405.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: use POST for save movie note

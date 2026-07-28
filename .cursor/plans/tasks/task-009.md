# Задача 009: Корректные HTTP-коды при недоступности Kinopoisk во views

## Проблема
Рендер `error.html` с HTTP 200 скрывает сбои интеграции от мониторинга и клиентов.

## Файл
`todo/views.py`

## Функция
`PreView.post / SaveView` (~49)

## Решение
Возвращать 502/503 (или 424) при ошибке внешнего API; оставить понятное сообщение пользователю в теле ответа.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: return proper status on kinopoisk failure

# Задача 028: Аутентификация и проверка владельца заметок (IDOR)

## Проблема
Все заметки видны всем; Detail/Delete по pk без владельца; User pk=1.

## Файл
`todo/views.py`

## Функция
`DetailView / DeleteView / SaveView` (~59)

## Решение
LoginRequiredMixin, фильтрация queryset по request.user, get_object с проверкой user; убрать pk=1.

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
feat: auth and note ownership checks

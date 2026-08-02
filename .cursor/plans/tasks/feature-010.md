# Задача feature-010: Убрать просмотренные фильмы со списка Watch later

## Проблема
`IndexView.get_context` показывает все заметки пользователя без учёта
`is_viewed` — после появления статуса Seen (feature-007) просмотренные
фильмы должны переехать в раздел Seen (feature-011), а не оставаться в
"Watch later" на главной.

## Файл
`todo/views.py` (~15-17, 49-54)

## Функция
`get_note_list` (~15), `IndexView.get_context` (~49)

## Решение
В `IndexView.get_context` фильтровать заметки по `is_viewed=False`:
`notes = get_note_list(request.user).filter(is_viewed=False)` (либо добавить
параметр `seen: bool` в `get_note_list` и передавать `False` из `IndexView`,
`True` — из `SeenView` в feature-011, чтобы не дублировать `select_related`).

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: exclude seen notes from the Watch later list

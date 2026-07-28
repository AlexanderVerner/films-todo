# Задача 021: select_related и очистка get_note_list

## Проблема
N+1 на главной; `get_note_list(self)` с лишним self и мёртвый except DoesNotExist.

## Файл
`todo/views.py`

## Функция
`get_note_list` (~9)

## Решение
`Note.objects.select_related('movie').filter(...)`; убрать ложную обработку исключений; сигнатура без фиктивного self.

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
refactor: optimize note list queryset

# Задача 015: JSONField default=list в models и миграция

## Проблема
Изменяемый `default=[]` в модели и истории миграций — риск общих списков между экземплярами.

## Файл
`todo/models.py`

## Функция
`Movie JSON fields` (~11)

## Решение
Заменить на `default=list`, сгенерировать новую миграцию AlterField (не править старые миграции вручную).

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: use callable default for JSONField

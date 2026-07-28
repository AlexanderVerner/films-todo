# Задача 024: Устранить дублирующиеся тесты SaveView

## Проблема
Два идентичных теста создают ложное покрытие.

## Файл
`todo/tests/test_view.py`

## Функция
`test_save_movie / test_get_detail_film` (~45)

## Решение
Оставить один осмысленный тест в правильном классе; явно создавать User в setUp/fixture.

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
refactor: remove duplicate save view tests

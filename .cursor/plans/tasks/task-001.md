# Задача 001: Исправить makemigrations для несуществующего app `tests`

## Проблема
При запуске `python run_tests.py todo` вызывается `makemigrations tests`, но приложения с меткой `tests` нет — раннер падает до прогона тестов.

## Файл
`run_tests.py`

## Функция
`run_tests` (~44)

## Решение
Убрать или исправить вызов `call_command("makemigrations", "tests", ...)`: мигрировать только реальные apps (`todo`) либо делать makemigrations опциональным флагом без неверной метки.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: correct test runner makemigrations target

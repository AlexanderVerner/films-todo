# Задача 014: Убрать eval из test-framework.sh

## Проблема
`eval "$condition"` — потенциальная command injection при расширении скрипта.

## Файл
`test-framework.sh`

## Функция
`check` (~9)

## Решение
Проверки как функции или `if`/`[ ]` без eval; сохранить текущее поведение счётчиков PASS/FAIL.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: remove eval from test-framework

# Задача 013: Починить подсчёт строк в analyze-project-structure.sh

## Проблема
Секция «Строки кода» пуста из-за падения `find -exec wc` и `2>/dev/null`.

## Файл
`.cursor/scripts/bash/analyze-project-structure.sh`

## Функция
`count_lines` (~8)

## Решение
Считать через `xargs`/`while read` или `rg --files` + `wc`; не глотать ошибки без fallback; адаптировать под Python вместо Go.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: reliable line count in analyze script

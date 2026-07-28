# Задача 018: Убрать нерабочий constance.backends.database из INSTALLED_APPS

## Проблема
Подключён бэкенд без приложения `constance` и настроек — мёртвая конфигурация.

## Файл
`_project_/settings.py`

## Функция
`INSTALLED_APPS` (~19)

## Решение
Удалить лишнюю запись или полноценно добавить constance с `CONSTANCE_*` — минимальный фикс: удалить.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: remove broken constance app entry

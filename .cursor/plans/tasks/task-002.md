# Задача 002: Заменить exec в run_tests_settings на importlib

## Проблема
`_project_/run_tests_settings.py` выполняет `exec("from %s.tests.settings import *" % app_name)` из argv — риск инъекции и хрупкая загрузка настроек.

## Файл
`_project_/run_tests_settings.py`

## Функция
`(модуль)` (~1)

## Решение
Использовать `importlib.import_module(f"{app_name}.tests.settings")` и явно копировать нужные имена в globals или задать `DJANGO_SETTINGS_MODULE` без exec.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: load test settings via importlib

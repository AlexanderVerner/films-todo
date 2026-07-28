# Задача 003: Вынести SECRET_KEY и DEBUG в переменные окружения

## Проблема
Секрет и `DEBUG = True` захардкожены в `_project_/settings.py` и дублируются в тестовых настройках; в docker это отдаёт трейсбеки наружу.

## Файл
`_project_/settings.py`

## Функция
`(модуль)` (~10)

## Решение
Читать `SECRET_KEY` и `DEBUG` через `envjson`/os.environ с безопасными dev-дефолтами только для локальной разработки; документировать переменные в `common.env` без коммита секретов.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: read SECRET_KEY and DEBUG from env

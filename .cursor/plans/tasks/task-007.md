# Задача 007: Обработка сетевых ошибок и JSONDecode в kinopoisk_get

## Проблема
Необработанные `ConnectionError`, `Timeout`, `JSONDecodeError` из `requests` и `json.loads` дают 500 без контекста.

## Файл
`todo/kinopoisk_api.py`

## Функция
`kinopoisk_get` (~18)

## Решение
Обернуть запрос и парсинг: логировать контекст, пробрасывать доменное исключение `raise KinopoiskApiError(...) from err` по соглашению base.md.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: handle network and json errors in kinopoisk_get

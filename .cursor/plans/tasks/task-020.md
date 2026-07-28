# Задача 020: Общий хелпер декодирования ответов Kinopoisk

## Проблема
Четыре `fetch_*` дублируют запрос→200→json.loads.

## Файл
`todo/kinopoisk_api.py`

## Функция
`fetch_film_details и др.` (~63)

## Решение
Вынести `_decode_json_response(response) -> dict|list` с единой обработкой ошибок поверх task-007/008.

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
refactor: deduplicate kinopoisk response decoding

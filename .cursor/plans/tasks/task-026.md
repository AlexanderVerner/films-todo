# Задача 026: Нормализовать контракт search_films / fetch_film_details

## Проблема
Успех — list/dict, ошибка — dict с `message`; хрупкая проверка в build_film_detail.

## Файл
`todo/kinopoisk_api.py`

## Функция
`search_films / build_film_detail` (~28)

## Решение
Ввести Result-тип или исключения; вызывающий код во views без isinstance на message.

## Промпт
`05b-refactor-complex.txt`

## Модель
Sonnet С thinking (medium)

## Commit
refactor: unify kinopoisk api return contract

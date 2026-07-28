# Задача 027: Слой services для заметок и интеграции Kinopoisk

## Проблема
Нет каталога services/ — пороги coverage из base.md недостижимы.

## Файл
`todo/`

## Функция
`(новый пакет services/)` (~1)

## Решение
Создать `todo/services/notes.py`, `todo/services/films.py`; views тонкие, бизнес-логика в сервисах с typing.Protocol при необходимости.

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
feat: add services layer for notes and films

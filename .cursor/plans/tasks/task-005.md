# Задача 005: Закрыть прямой доступ к Django на порту 8000

## Проблема
Публикация `8000:8000` обходит nginx и TLS; при DEBUG=True приложение доступно напрямую.

## Файл
`docker-compose.yml`

## Функция
`services.web` (~21)

## Решение
Убрать mapping порта 8000 на хост или ограничить `expose` только для внутренней сети compose; трафик только через nginx.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: stop exposing django port on host

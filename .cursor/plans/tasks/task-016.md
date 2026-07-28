# Задача 016: Подключить nginx.conf вместо неиспользуемого .template

## Проблема
Конфиг монтируется как `web.template` и не подхватывается nginx.

## Файл
`docker-compose.yml`

## Функция
`services.nginx` (~2)

## Решение
Монтировать в `conf.d/default.conf` или entrypoint с `envsubst`; убедиться, что конфиг из репозитория реально загружается.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: apply nginx config in compose

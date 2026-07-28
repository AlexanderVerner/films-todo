# Задача 017: Исправить CORS, SSL и маршрутизацию proxy в nginx

## Проблема
Отражение Origin с credentials, 443 без сертификатов, `@proxy` не используется — сервис недоступен.

## Файл
`_local_deploy/nginx.conf`

## Функция
`server :443` (~20)

## Решение
Явный whitelist Origin или убрать credentials; dev-сертификаты или отдельный :80 proxy; `location /` → proxy_pass; определить `log_format` или убрать logextra.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: secure cors ssl and proxy routes in nginx

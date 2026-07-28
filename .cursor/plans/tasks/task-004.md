# Задача 004: Убрать захардкоженный пароль PostgreSQL из docker-compose

## Проблема
Пароль БД закоммичен в `docker-compose.yml`, что нарушает политику секретов из base.md.

## Файл
`docker-compose.yml`

## Функция
`services.postgresdb` (~38)

## Решение
Передавать `POSTGRES_PASSWORD` через `env_file` / переменные из `.env`; убрать литерал пароля из репозитория.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: externalize postgres password in compose

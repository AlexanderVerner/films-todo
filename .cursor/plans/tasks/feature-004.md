# Задача feature-004: Регистрация пользователя + состояние навбара

## Проблема
Создать нового пользователя можно только через `manage.py createsuperuser`
(или миграцию `0002`) — самостоятельной регистрации нет. В навбаре
(`base.html`) нет ссылок Login/Register/Logout — только пункты Watch
later/Watch today/Seen.

## Файл
`todo/forms.py`, `todo/views.py`, `todo/urls.py`, `_project_/templates/todo/register.html` (новый), `_project_/templates/todo/base.html` (~60-73)

## Функция
`(новая) RegisterForm`, `(новая) RegisterView`, navbar `<ul class="nav navbar-nav navbar-right">` (~66)

## Решение
1. `RegisterForm(UserCreationForm)` в `todo/forms.py` с дополнительным полем
   `email` (обязательное), стилизованными виджетами (`class: form-control`,
   как в `SearchForm`).
2. `RegisterView(View).post/get` в `todo/views.py`: на GET — рендер формы, на
   POST — валидация, создание `User`, `login(request, user)`, redirect на
   `todo:index`.
3. `register.html` — тот же блок `auth` и визуальный стиль, что и
   `login.html` (feature-003), ссылка "Уже есть аккаунт? Войти".
4. В `base.html` обернуть пункты меню в `{% if user.is_authenticated %}` —
   показывать `Logout` (POST-форма или ссылка на `todo:logout`) и имя
   пользователя; для анонимов показывать `Login`/`Register`
   (`{% url 'todo:login' %}` / `{% url 'todo:register' %}`).

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
feat: add user registration and auth-aware navbar

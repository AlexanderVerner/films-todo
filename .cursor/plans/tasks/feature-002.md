# Задача feature-002: Свои URL и настройки авторизации вместо admin:login

## Проблема
Логин сейчас идёт через стандартную Django-админку: каждая LoginRequiredMixin
вью (`IndexView`, `PreView`, `DetailView`, `SaveView`, `DeleteView`) явно
задаёт `login_url = 'admin:login'`. Централизованного `LOGIN_URL` нет, своих
`login`/`logout`/`register` маршрутов в приложении тоже нет.

## Файл
`_project_/settings_base.py`, `_project_/urls.py`, `todo/urls.py`, `todo/views.py`

## Функция
`BASE_INSTALLED_APPS`/модуль настроек (~33); `login_url` в `IndexView` (~44),
`PreView` (~59), `DetailView` (~75), `SaveView` (~83), `DeleteView` (~104)

## Решение
1. В `_project_/settings_base.py` добавить `LOGIN_URL = 'todo:login'`,
   `LOGIN_REDIRECT_URL = 'todo:index'`, `LOGOUT_REDIRECT_URL = 'todo:login'`.
2. В `todo/urls.py` добавить маршруты `login` → `django.contrib.auth.views.LoginView`
   (template_name будет задан в feature-003), `logout` →
   `django.contrib.auth.views.LogoutView`, `register` → новый `RegisterView`
   (реализация в feature-004, здесь достаточно заглушки/импорта).
3. Убрать `login_url = 'admin:login'` из всех вью в `todo/views.py` —
   `LoginRequiredMixin` возьмёт `settings.LOGIN_URL` по умолчанию.
4. Проверить, что `admin:login` больше нигде не используется как fallback.

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
feat: wire dedicated login/logout/register routes instead of admin login

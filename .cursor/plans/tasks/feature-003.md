# Задача feature-003: Дизайн страницы Login в стиле темы

## Проблема
Своей страницы логина нет (см. feature-002) — нужен экран в едином визуальном
стиле с остальным приложением (используется тема с hero-секциями,
`.form-control`, `.btn-round`, `.callout-*` в `style.css`), а не голая форма.

## Файл
`_project_/templates/todo/login.html` (новый), `_project_/templates/todo/base.html` (~74-77), `todo/urls.py`

## Функция
`{% block auth %}` (новый блок в base.html)

## Решение
1. В `base.html` добавить ещё один опциональный `{% block auth %}{% endblock %}`
   рядом с существующими `content`/`preview`/`detail`/`error`.
2. Создать `login.html` (`{% extends 'todo/base.html' %}`, `{% block auth %}`):
   секция на фоне hero (переиспользовать `.home-section`/`.bg-dark-30` как в
   `index.html`), по центру карточка формы (`.callout-btn-box`) с полями
   username/password (`{{ form.username }}`, `{{ form.password }}`,
   `class="form-control"`), кнопка `btn btn-g btn-round`, вывод
   `{{ form.errors }}`/`{{ form.non_field_errors }}`, ссылка на регистрацию
   (`{% url 'todo:register' %}`).
3. В `todo/urls.py` задать `LoginView.as_view(template_name='todo/login.html')`.

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
feat: add themed login page

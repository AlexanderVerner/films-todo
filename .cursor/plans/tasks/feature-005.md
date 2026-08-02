# Задача feature-005: Кнопка Watch today — случайный непросмотренный фильм

## Проблема
Пункт меню "Watch today" в `base.html` (~68) ведёт на `href="#"` —
функциональности нет.

## Файл
`todo/views.py` (новая `WatchTodayView`), `todo/urls.py`, `_project_/templates/todo/base.html` (~68)

## Функция
`get_note_list` (~15, переиспользуется)

## Решение
1. `WatchTodayView(LoginRequiredMixin, View).get` в `todo/views.py`:
   `notes = list(get_note_list(request.user).filter(is_viewed=False))`; если
   пусто — `messages.info(...)` + redirect на `todo:index`; иначе
   `random.choice(notes)` и redirect на `todo:detail` с `note.id`.
2. Добавить маршрут `watch-today` в `todo/urls.py` (`name='watch-today'`).
3. Заменить `href="#"` у пункта "Watch today" в `base.html` на
   `{% url 'todo:watch-today' %}`.

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
feat: implement Watch today as a random unwatched pick

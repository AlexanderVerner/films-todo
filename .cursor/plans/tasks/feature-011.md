# Задача feature-011: Страница Seen — список, сортировка, фильтр по жанру

## Проблема
Раздела Seen не существует: пункт меню в `base.html` (~69) ведёт на `href="#"`,
`SeenView` закомментирован в `todo/views.py` (~112) и `todo/urls.py` (~11).
Просмотренные фильмы с оценкой и отзывом просмотреть негде.

## Файл
`todo/views.py` (новая `SeenView`), `todo/urls.py`, `_project_/templates/todo/seen.html` (новый), `_project_/templates/todo/includes/movie_card.html` (из feature-001), `_project_/templates/todo/base.html` (~69)

## Функция
`(закомментированный) SeenView` (~112)

## Решение
1. `SeenView(LoginRequiredMixin, TemplateView).get` в `todo/views.py`:
   `notes = get_note_list(request.user).filter(is_viewed=True)`; поддержать
   query-параметры `sort` (`rating`/`-rating`/`date`/`-date`, по умолчанию
   `-created`) и `genre` (фильтр по вхождению в `movie.genres`); собрать
   список доступных жанров пользователя для фильтра.
2. `seen.html` переиспользует `includes/movie_card.html` (feature-001),
   расширенный необязательным блоком: бейдж оценки (`render_user_stars` из
   feature-009) и обрезанный `note.review`; над сеткой — переключатели
   сортировки и select с жанрами (форма `method="get"`, сохраняющая текущие
   параметры).
3. Добавить маршрут `seen` в `todo/urls.py`, заменить `href="#"` у пункта
   "Seen" в `base.html` на `{% url 'todo:seen' %}`.

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
feat: add Seen page with sorting and genre filter

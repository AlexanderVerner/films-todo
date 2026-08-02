# Задача feature-009: Рендер оценки пользователя, скрытой пока не оценено

## Проблема
Блок звёзд под заголовком фильма в `detail.html` (~24-33) захардкожен: 4
закрашенные звезды из 5 показываются всегда, независимо от того, ставил ли
пользователь свою оценку.

## Файл
`todo/templatetags/todo_extras.py`, `_project_/templates/todo/detail.html` (~24-33, ~105)

## Функция
`(новый) render_user_stars` в `todo_extras.py`

## Решение
1. Добавить в `todo_extras.py` inclusion tag/filter `render_user_stars(rating)`,
   рисующий 10 иконок `<i class="fa fa-star star">`/`star-off` по значению
   `rating` (1-10), аналогично существующему `format_rating`.
2. В `detail.html` обернуть блок рейтинга в
   `{% if note.user_rating > 0 %}` (используя `render_user_stars` вместо
   хардкода), иначе секция не выводится вовсе — требование "до того как
   оценка не выставлена, отображать не нужно".
3. Добавить `id="reviews"` на секцию "Add review" (~105), чтобы ссылка
   `<a class="open-tab section-scroll" href="#reviews">` реально скроллила к
   форме.

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
feat: render user rating as stars, hidden until rated

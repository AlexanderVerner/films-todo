# Задача feature-007: Форма отзыва + view отметки Seen/Un-seen

## Проблема
`SeenView` и маршрут `review/<int:note_id>` закомментированы в
`todo/views.py` (~112-118) и `todo/urls.py` (~11) — сохранить оценку/отзыв и
отметить фильм просмотренным нечем.

## Файл
`todo/forms.py` (новая `ReviewForm`), `todo/views.py` (новая `ReviewView`, `UnseeView`), `todo/urls.py`

## Функция
`(закомментированный) SeenView` (~112)

## Решение
1. `ReviewForm(forms.Form)` в `todo/forms.py`: `rating = IntegerField(min_value=1, max_value=10)`,
   `review = CharField(widget=Textarea, required=False)`.
2. `ReviewView(LoginRequiredMixin, View).post` в `todo/views.py`: находит
   `Note` по `note_id` и `user=request.user` (404 иначе, без IDOR), валидирует
   `ReviewForm`, сохраняет `user_rating`, `review`, `is_viewed=True`, redirect
   на `todo:detail`. При невалидной форме — повторный рендер `detail.html` с
   ошибками.
3. `UnseeView(LoginRequiredMixin, View).post`: тот же lookup по `note_id`+`user`,
   `note.is_viewed = False; note.save()` (оценка и отзыв не удаляются),
   redirect на `todo:detail`.
4. Раскомментировать/переписать маршруты в `todo/urls.py`:
   `review/<int:note_id>` (name=`review`) → `ReviewView`,
   `review/<int:note_id>/unsee` (name=`unsee`) → `UnseeView`.

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
feat: add review submission and seen/unsee views

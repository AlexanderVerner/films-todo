# Задача feature-008: Починить разметку Add Review + интерактивные 10 звёзд

## Проблема
В `detail.html` форма "Add review" (~105-137) вложена внутрь формы удаления
(~8), а `<select>` (~111) и `<textarea>` (~128) не имеют атрибута `name` —
данные физически не могут дойти до сервера. Рейтинг задаётся выпадающим
списком чисел, а не звёздами, как требуется по продукту.

## Файл
`_project_/templates/todo/detail.html` (~8, ~105-137)

## Функция
блок "Add review" / форма удаления (~8, ~139)

## Решение
1. Разнести формы: убрать вложенность (форма удаления и форма отзыва — два
   независимых `<form>` на одном уровне, как уже сделано для формы удаления
   внизу файла).
2. Форма отзыва теперь ведёт на `{% url 'todo:review' note.id %}` (feature-007),
   поле рейтинга — 10 кликабельных иконок `fa-star`/`.star`/`.star-off`
   (например через 10 `<input type="radio" name="rating" value="N">` +
   `<label>` с CSS `:checked ~ label`/hover подсветкой, стили рядом в
   `style.css` или новый `todo/css/rating-widget.css`), поле отзыва —
   `<textarea name="review">`, оба предзаполнены текущими
   `note.user_rating`/`note.review`.
3. Текст кнопки: "Seen", если `note.user_rating == 0`, иначе "Update review".
4. Если `note.is_viewed`, добавить вторую кнопку/форму "Move to Watch later"
   (POST на `{% url 'todo:unsee' note.id %}`).

## Промпт
`04-create-architecture.txt`

## Модель
Sonnet БЕЗ thinking

## Commit
fix: repair review form markup and add clickable star rating input

# Задача feature-001: Починить сетку фильмов на главной странице

## Проблема
Список заметок на главной (`{% for item in note_list %}`) рендерится через
Bootstrap 3 float-колонки (`row multi-columns-row post-columns`,
`col-sm-6 col-md-4 col-lg-4`). Класс `multi-columns-row` нигде не описан в
`style.css` — это мёртвая заготовка под clearfix, которая не работает.
Карточки имеют разную высоту (заголовок в 1-2 строки, разная длина описания),
float-грид этого не учитывает — как только высоты соседних карточек
расходятся, следующие элементы "уезжают" вправо/налево от ожидаемой позиции
вместо аккуратных рядов.

## Файл
`_project_/templates/todo/index.html` (~62-88)

## Функция
`{% block content %}` — секция notes (~41-91)

## Решение
1. Заменить float-грид на flexbox: контейнер карточек — `display: flex;
   flex-wrap: wrap;` с `align-items: stretch`, каждая карточка — фиксированная
   доля ширины через `flex: 0 0 …%` на нужных брейкпоинтах (аналог текущих
   `col-sm-6 col-md-4 col-lg-4`), либо `display: grid;
   grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))`. Стили
   добавить новым блоком в `_project_/static/todo/css/style.css` (класс
   `.movies-grid` / `.movie-card`), убрать использование нерабочего
   `multi-columns-row`.
2. Вынести разметку одной карточки в переиспользуемый partial
   `_project_/templates/todo/includes/movie_card.html`, принимающий `note` в
   контексте (poster, title, meta, description, ссылка на detail). Заинклюдить
   его в `index.html` через `{% include %}` — этот же partial переиспользует
   feature-011 (страница Seen).
3. Убедиться, что карточки одинаковой высоты в ряду (stretch) и при 1/2/3
   колонках на разных брейкпоинтах ничего не "прыгает".

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
fix: replace broken float grid on homepage with flexbox/grid layout

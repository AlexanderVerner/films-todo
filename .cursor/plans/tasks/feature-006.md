# Задача feature-006: Поле review и валидация рейтинга в Note

## Проблема
`Note.review` закомментирован (~37), функциональности отзыва в модели нет.
`user_rating` — `PositiveIntegerField(default=0)` без верхней границы, хотя по
продукту шкала строго 1-10.

## Файл
`todo/models.py` (~31-40)

## Функция
`Note` (~31)

## Решение
1. Раскомментировать и включить `review = models.TextField(blank=True, default='')`.
2. Добавить `validators=[MinValueValidator(1), MaxValueValidator(10)]` на
   `user_rating` (диапазон 1-10; `default=0` сохранить как маркер "оценки нет" —
   в шаблонах/вью проверять `note.user_rating > 0`, а не `is_viewed`, чтобы
   отличать "оценено" от "не оценено").
3. Сгенерировать и применить миграцию `0005_note_review_rating_validators.py`.

## Промпт
`05-refactor.txt`

## Модель
Haiku С thinking

## Commit
feat: add review field and rating validators to Note

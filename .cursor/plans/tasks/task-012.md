# Задача 012: Исправить вложенные формы и разметку detail.html

## Проблема
Вложенные `<form>` и сломанный баланс div ломают Delete/Seen в браузере.

## Файл
`_project_/templates/todo/detail.html`

## Функция
`{% block detail %}` (~8)

## Решение
Одна форма на действие, кнопки через отдельные form вне вложенности; выровнять открывающие/закрывающие теги.

## Промпт
`03-fix-simple-bug.txt`

## Модель
Haiku БЕЗ thinking

## Commit
fix: repair detail template forms and markup

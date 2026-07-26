from django.test import SimpleTestCase

from todo.templatetags.todo_extras import (
    format_person_list,
    format_rating,
    format_watchability,
)


class FormatPersonListFilterTests(SimpleTestCase):

    def test_legacy_dict_format(self):
        people = [
            {'Пол Уокер': 'Paul Walker'},
            {'Вин Дизель': 'Vin Diesel'},
        ]
        self.assertEqual(
            format_person_list(people),
            'Пол Уокер / Paul Walker, Вин Дизель / Vin Diesel',
        )

    def test_string_format(self):
        people = ['Пол Уокер / Paul Walker', 'Вин Дизель / Vin Diesel']
        self.assertEqual(
            format_person_list(people),
            'Пол Уокер / Paul Walker, Вин Дизель / Vin Diesel',
        )


class FormatWatchabilityFilterTests(SimpleTestCase):

    def test_renders_platform_links(self):
        sources = [{
            'name': 'Okko',
            'url': 'https://okko.tv/serial/the-office?utm_medium=referral',
        }]
        rendered = format_watchability(sources)
        self.assertIn('href="https://okko.tv/serial/the-office?utm_medium=referral"', rendered)
        self.assertIn('>Okko</a>', rendered)
        self.assertIn('rel="noopener noreferrer"', rendered)


class FormatRatingFilterTests(SimpleTestCase):

    def test_trims_decimal_places(self):
        self.assertEqual(format_rating('8.7000'), '8.7')

    def test_whole_number_without_fraction(self):
        self.assertEqual(format_rating('8.0'), '8')


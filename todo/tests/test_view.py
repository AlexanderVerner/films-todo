from django.test import TestCase
from django.urls import reverse
from todo.models import Movie


class SaveViewTests(TestCase):

    def test_get_detail_film(self):
        r = self.client.get(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        movie = Movie.objects.get(id_kinopoisk=409424)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(movie.title, 'Дюна')

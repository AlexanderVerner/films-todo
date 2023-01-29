from django.test import TestCase
from django.urls import reverse
from todo.models import Movie


class IndexViewTests(TestCase):

    def test_get_index_view(self):
        r = self.client.get(reverse('todo:index'))
        self.assertEqual(r.status_code, 200)


class PreViewTests(TestCase):

    def test_get_preview_view(self):
        r = self.client.get(reverse('todo:preview'))
        self.assertEqual(r.status_code, 200)

    def test_save_movie(self):
        r = self.client.get(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        movie = Movie.objects.get(id_kinopoisk=409424)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(movie.title, 'Дюна')


class SaveViewTests(TestCase):

    def test_get_detail_film(self):
        r = self.client.get(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        movie = Movie.objects.get(id_kinopoisk=409424)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(movie.title, 'Дюна')

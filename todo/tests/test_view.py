from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from todo.models import Movie


DUNE_DETAIL = {
    'id_kinopoisk': 409424,
    'film': 'Дюна',
    'film_alternative': 'Dune',
    'type': 'FILM',
    'year': 2021,
    'slogan': None,
    'description': 'Test description',
    'genres': ['фантастика'],
    'age_rating': 12,
    'countries': ['США'],
    'poster': 'https://example.com/poster.jpg',
    'rating_kp': 7.9,
    'rating_imdb': 8.0,
    'votes_kp': 100,
    'votes_imdb': 200,
    'premiere_world': None,
    'premiere_russia': None,
    'watchability': [],
    'actors': [],
    'directors': [],
}


class IndexViewTests(TestCase):

    def test_get_index_view(self):
        r = self.client.get(reverse('todo:index'))
        self.assertEqual(r.status_code, 200)


class PreViewTests(TestCase):

    def test_get_preview_view(self):
        r = self.client.get(reverse('todo:preview'))
        self.assertEqual(r.status_code, 200)

    @patch('todo.views.build_film_detail', return_value=DUNE_DETAIL)
    def test_save_movie(self, _mock_detail):
        r = self.client.get(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        movie = Movie.objects.get(id_kinopoisk=409424)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(movie.title, 'Дюна')


class SaveViewTests(TestCase):

    @patch('todo.views.build_film_detail', return_value=DUNE_DETAIL)
    def test_get_detail_film(self, _mock_detail):
        r = self.client.get(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        movie = Movie.objects.get(id_kinopoisk=409424)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(movie.title, 'Дюна')

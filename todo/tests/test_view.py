from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from todo.kinopoisk_api import KinopoiskApiError
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

API_ERROR = KinopoiskApiError('Please, check your configuration.')


class IndexViewTests(TestCase):

    def test_get_index_view(self):
        r = self.client.get(reverse('todo:index'))
        self.assertEqual(r.status_code, 200)


class PreViewTests(TestCase):

    def test_get_preview_view(self):
        r = self.client.get(reverse('todo:preview'))
        self.assertEqual(r.status_code, 200)

    @patch('todo.views.get_preview_content')
    def test_preview_search_success(self, mock_search):
        mock_search.return_value = [
            {'id_kinopoisk': 409424, 'film': 'Дюна'}
        ]
        r = self.client.post(reverse('todo:preview'), {'title': 'dune'})
        self.assertEqual(r.status_code, 200)

    @patch('todo.views.get_preview_content')
    def test_preview_api_error_returns_503(self, mock_search):
        """PreView.post should return 503 when the API layer raises"""
        mock_search.side_effect = API_ERROR
        r = self.client.post(reverse('todo:preview'), {'title': 'dune'})
        self.assertEqual(r.status_code, 503)
        self.assertIn(b'Please, check your configuration', r.content)


class SaveViewTests(TestCase):

    def setUp(self):
        """Create User with pk=1 for testing SaveView"""
        User.objects.create_user(username='testuser', password='testpass123')

    @patch('todo.views.build_film_detail', return_value=DUNE_DETAIL)
    def test_post_save_movie(self, _mock_detail):
        """SaveView.post should save movie and redirect on success"""
        r = self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        movie = Movie.objects.get(id_kinopoisk=409424)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(movie.title, 'Дюна')

    @patch('todo.views.get_detail_film')
    def test_save_api_error_returns_503(self, mock_detail):
        """SaveView.post should return 503 when the API layer raises"""
        mock_detail.side_effect = API_ERROR
        r = self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        self.assertEqual(r.status_code, 503)
        self.assertIn(b'Please, check your configuration', r.content)
        self.assertFalse(Movie.objects.filter(id_kinopoisk=409424).exists())

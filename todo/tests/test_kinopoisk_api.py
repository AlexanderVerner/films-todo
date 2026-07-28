import json
from datetime import date
from unittest import TestCase
from unittest.mock import MagicMock, patch
import requests

from todo.kinopoisk_api import (
    build_film_detail,
    KinopoiskApiError,
    kinopoisk_get,
    premiere_dates_from_distributions,
    search_films,
    watchability_from_external_sources,
    fetch_film_details,
    fetch_film_staff,
    fetch_film_distributions,
    fetch_film_external_sources,
)


class KinopoiskApiMappingTests(TestCase):

    def test_premiere_dates_from_distributions(self):
        distributions = {
            'items': [
                {'type': 'WORLD_PREMIER', 'date': '2021-09-15', 'country': None},
                {
                    'type': 'PREMIERE',
                    'date': '2021-10-14',
                    'country': {'country': 'Россия'},
                },
            ]
        }
        world, russia = premiere_dates_from_distributions(distributions)
        self.assertEqual(world, date(2021, 9, 15))
        self.assertEqual(russia, date(2021, 10, 14))

    def test_watchability_from_external_sources(self):
        external = {
            'items': [
                {'platform': 'Okko', 'url': 'https://okko.tv/movie/1'},
            ]
        }
        self.assertEqual(
            watchability_from_external_sources(external),
            [{'name': 'Okko', 'url': 'https://okko.tv/movie/1'}],
        )

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_maps_unofficial_response(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [{
                    'filmId': 409424,
                    'nameRu': 'Дюна',
                    'year': '2021',
                    'description': 'USA, Denis Villeneuve',
                    'posterUrlPreview': 'https://example.com/poster.jpg',
                    'rating': '7.9',
                }],
            }).encode(),
        )
        result = search_films('dune', 15)
        mock_get.assert_called_once_with(
            '/api/v2.1/films/search-by-keyword',
            params={'keyword': 'dune', 'page': 1},
        )
        self.assertEqual(result[0]['id_kinopoisk'], 409424)
        self.assertEqual(result[0]['film'], 'Дюна')
        self.assertEqual(result[0]['rating_kp'], 7.9)

    @patch('todo.kinopoisk_api.fetch_film_external_sources')
    @patch('todo.kinopoisk_api.fetch_film_distributions')
    @patch('todo.kinopoisk_api.fetch_film_staff')
    @patch('todo.kinopoisk_api.fetch_film_details')
    def test_build_film_detail(
        self,
        mock_details,
        mock_staff,
        mock_distributions,
        mock_external,
    ):
        mock_details.return_value = {
            'kinopoiskId': 409424,
            'nameRu': 'Дюна',
            'nameEn': 'Dune',
            'type': 'FILM',
            'year': 2021,
            'description': 'Desc',
            'genres': [{'genre': 'фантастика'}],
            'countries': [{'country': 'США'}],
            'ratingKinopoisk': 7.9,
            'ratingImdb': 8.0,
            'ratingKinopoiskVoteCount': 100,
            'ratingImdbVoteCount': 200,
            'posterUrlPreview': 'https://example.com/poster.jpg',
        }
        mock_staff.return_value = [
            {'professionKey': 'ACTOR', 'nameRu': 'Actor', 'nameEn': 'Actor En'},
            {'professionKey': 'DIRECTOR', 'nameRu': 'Director', 'nameEn': 'Dir En'},
        ]
        mock_distributions.return_value = {'items': []}
        mock_external.return_value = {'items': []}

        detail = build_film_detail(409424)
        self.assertEqual(detail['id_kinopoisk'], 409424)
        self.assertEqual(detail['film'], 'Дюна')
        self.assertEqual(detail['genres'], ['фантастика'])
        self.assertEqual(detail['actors'], ['Actor / Actor En'])
        self.assertEqual(detail['directors'], ['Director / Dir En'])

    @patch('todo.kinopoisk_api.requests.get')
    def test_kinopoisk_get_handles_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError('Connection failed')
        
        with self.assertRaises(KinopoiskApiError) as ctx:
            kinopoisk_get('/api/v2.1/films/search', params={'keyword': 'test'})
        
        self.assertIn('Failed to fetch from Kinopoisk API', str(ctx.exception))
        self.assertIsNotNone(ctx.exception.__cause__)

    @patch('todo.kinopoisk_api.requests.get')
    def test_kinopoisk_get_handles_timeout(self, mock_get):
        mock_get.side_effect = requests.Timeout('Request timeout')
        
        with self.assertRaises(KinopoiskApiError) as ctx:
            kinopoisk_get('/api/v2.1/films/search', params={'keyword': 'test'})
        
        self.assertIn('Failed to fetch from Kinopoisk API', str(ctx.exception))
        self.assertIsNotNone(ctx.exception.__cause__)

    @patch('todo.kinopoisk_api.requests.get')
    def test_kinopoisk_get_handles_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError('404 Not Found')
        mock_get.return_value = mock_response
        
        with self.assertRaises(KinopoiskApiError) as ctx:
            kinopoisk_get('/api/v2.1/films/999999')
        
        self.assertIn('Failed to fetch from Kinopoisk API', str(ctx.exception))
        self.assertIsNotNone(ctx.exception.__cause__)

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_handles_json_decode_error(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=b'invalid json {',
        )
        
        result = search_films('test', 15)
        self.assertEqual(result, {'message': 'Please, check your configuration.'})

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_handles_api_error(self, mock_get):
        mock_get.side_effect = KinopoiskApiError('API Error')
        
        result = search_films('test', 15)
        self.assertEqual(result, {'message': 'Please, check your configuration.'})

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_details_handles_api_error(self, mock_get):
        mock_get.side_effect = KinopoiskApiError('API Error')
        
        result = fetch_film_details(409424)
        self.assertEqual(result, {'message': 'Please, check your configuration.'})

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_staff_handles_api_error(self, mock_get):
        mock_get.side_effect = KinopoiskApiError('API Error')
        
        result = fetch_film_staff(409424)
        self.assertEqual(result, [])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_distributions_handles_api_error(self, mock_get):
        mock_get.side_effect = KinopoiskApiError('API Error')
        
        result = fetch_film_distributions(409424)
        self.assertEqual(result, {})

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_external_sources_handles_api_error(self, mock_get):
        mock_get.side_effect = KinopoiskApiError('API Error')
        
        result = fetch_film_external_sources(409424)
        self.assertEqual(result, {})

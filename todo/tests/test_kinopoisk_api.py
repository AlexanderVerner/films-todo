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
    parse_age_rating,
    staff_by_profession,
    format_person_name,
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

    @patch('todo.kinopoisk_api.fetch_film_external_sources', return_value={'items': []})
    @patch('todo.kinopoisk_api.fetch_film_distributions', return_value={'items': []})
    @patch('todo.kinopoisk_api.fetch_film_staff', return_value=[])
    @patch('todo.kinopoisk_api.fetch_film_details')
    def test_build_film_detail_accepts_payload_with_message_field(
        self,
        mock_details,
        _mock_staff,
        _mock_distributions,
        _mock_external,
    ):
        """A `message` key in a successful payload is regular data, not an error."""
        mock_details.return_value = {
            'kinopoiskId': 409424,
            'nameRu': 'Дюна',
            'message': 'some field the API happens to return',
        }

        detail = build_film_detail(409424)
        self.assertEqual(detail['id_kinopoisk'], 409424)
        self.assertEqual(detail['film'], 'Дюна')

    @patch('todo.kinopoisk_api.fetch_film_details')
    def test_build_film_detail_propagates_api_error(self, mock_details):
        mock_details.side_effect = KinopoiskApiError('Please, check your configuration.')

        with self.assertRaises(KinopoiskApiError):
            build_film_detail(409424)

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

        with self.assertRaises(KinopoiskApiError) as ctx:
            search_films('test', 15)
        self.assertEqual(str(ctx.exception), 'Please, check your configuration.')

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_handles_api_error(self, mock_get):
        mock_get.side_effect = KinopoiskApiError('API Error')

        with self.assertRaises(KinopoiskApiError) as ctx:
            search_films('test', 15)
        self.assertEqual(str(ctx.exception), 'Please, check your configuration.')

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_rejects_non_object_payload(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps([1, 2, 3]).encode(),
        )

        with self.assertRaises(KinopoiskApiError) as ctx:
            search_films('test', 15)
        self.assertEqual(str(ctx.exception), 'Please, check your configuration.')

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_returns_list_on_empty_results(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({'films': []}).encode(),
        )

        self.assertEqual(search_films('nothing', 15), [])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_details_handles_api_error(self, mock_get):
        mock_get.side_effect = KinopoiskApiError('API Error')

        with self.assertRaises(KinopoiskApiError) as ctx:
            fetch_film_details(409424)
        self.assertEqual(str(ctx.exception), 'Please, check your configuration.')

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_details_handles_malformed_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=b'invalid json {',
        )

        with self.assertRaises(KinopoiskApiError):
            fetch_film_details(409424)

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_details_rejects_non_object_payload(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps([1, 2, 3]).encode(),
        )

        with self.assertRaises(KinopoiskApiError):
            fetch_film_details(409424)

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_staff_handles_api_error(self, mock_get):
        mock_get.side_effect = KinopoiskApiError('API Error')
        
        result = fetch_film_staff(409424)
        self.assertEqual(result, [])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_staff_returns_list_on_unexpected_payload(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({'unexpected': 'shape'}).encode(),
        )

        self.assertEqual(fetch_film_staff(409424), [])

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


class KinopoiskApiErrorHandlingTests(TestCase):
    """Tests for error paths, boundary values, and helper functions."""

    @patch('todo.kinopoisk_api.requests.get')
    def test_kinopoisk_get_handles_404_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError('404 Not Found')
        mock_get.return_value = mock_response

        with self.assertRaises(KinopoiskApiError) as ctx:
            kinopoisk_get('/api/v2.2/films/999999')

        self.assertIn('Failed to fetch from Kinopoisk API', str(ctx.exception))

    @patch('todo.kinopoisk_api.requests.get')
    def test_kinopoisk_get_handles_500_internal_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError('500 Internal Server Error')
        mock_get.return_value = mock_response

        with self.assertRaises(KinopoiskApiError) as ctx:
            kinopoisk_get('/api/v2.1/films/search')

        self.assertIn('Failed to fetch from Kinopoisk API', str(ctx.exception))

    @patch('todo.kinopoisk_api.requests.get')
    def test_kinopoisk_get_handles_429_too_many_requests(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError('429 Too Many Requests')
        mock_get.return_value = mock_response

        with self.assertRaises(KinopoiskApiError) as ctx:
            kinopoisk_get('/api/v2.1/films/search')

        self.assertIn('Failed to fetch from Kinopoisk API', str(ctx.exception))

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_with_zero_limit(self, mock_get):
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
        result = search_films('dune', 0)
        self.assertEqual(result, [])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_with_large_limit(self, mock_get):
        films = [
            {
                'filmId': 409424 + i,
                'nameRu': f'Фильм {i}',
                'year': '2021',
                'description': f'Description {i}',
                'rating': '7.9',
            }
            for i in range(100)
        ]
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({'films': films}).encode(),
        )
        result = search_films('test', 1000)
        self.assertEqual(len(result), 100)

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_filters_items_missing_description(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [
                    {
                        'filmId': 409424,
                        'nameRu': 'Дюна',
                        'year': '2021',
                        'description': 'Valid description',
                        'rating': '7.9',
                    },
                    {
                        'filmId': 409425,
                        'nameRu': 'Другой фильм',
                        'year': '2021',
                        'description': None,
                        'rating': '8.0',
                    },
                ],
            }).encode(),
        )
        result = search_films('test', 10)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id_kinopoisk'], 409424)

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_filters_items_missing_year(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [
                    {
                        'filmId': 409424,
                        'nameRu': 'Дюна',
                        'year': None,
                        'description': 'Valid description',
                        'rating': '7.9',
                    },
                ],
            }).encode(),
        )
        result = search_films('test', 10)
        self.assertEqual(result, [])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_handles_invalid_year_format(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [
                    {
                        'filmId': 409424,
                        'nameRu': 'Дюна',
                        'year': 'not_a_year',
                        'description': 'Valid description',
                        'rating': '7.9',
                    },
                ],
            }).encode(),
        )
        result = search_films('test', 10)
        self.assertEqual(result, [])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_handles_invalid_rating_format(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [
                    {
                        'filmId': 409424,
                        'nameRu': 'Дюна',
                        'year': '2021',
                        'description': 'Valid description',
                        'rating': 'not_a_rating',
                    },
                ],
            }).encode(),
        )
        result = search_films('test', 10)
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]['rating_kp'])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_handles_empty_string_rating(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [
                    {
                        'filmId': 409424,
                        'nameRu': 'Дюна',
                        'year': '2021',
                        'description': 'Valid description',
                        'rating': '',
                    },
                ],
            }).encode(),
        )
        result = search_films('test', 10)
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]['rating_kp'])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_uses_fallback_poster_url(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [
                    {
                        'filmId': 409424,
                        'nameRu': 'Дюна',
                        'year': '2021',
                        'description': 'Valid',
                        'posterUrlPreview': None,
                        'posterUrl': 'https://example.com/fallback.jpg',
                        'rating': '7.9',
                    },
                ],
            }).encode(),
        )
        result = search_films('test', 10)
        self.assertEqual(result[0]['poster'], 'https://example.com/fallback.jpg')

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_uses_default_poster_when_both_missing(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [
                    {
                        'filmId': 409424,
                        'nameRu': 'Дюна',
                        'year': '2021',
                        'description': 'Valid',
                        'posterUrlPreview': None,
                        'posterUrl': None,
                        'rating': '7.9',
                    },
                ],
            }).encode(),
        )
        result = search_films('test', 10)
        self.assertIn('i.ibb.co', result[0]['poster'])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_search_films_uses_nameEn_fallback(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({
                'films': [
                    {
                        'filmId': 409424,
                        'nameRu': None,
                        'nameEn': 'Dune',
                        'year': '2021',
                        'description': 'Valid',
                        'rating': '7.9',
                    },
                ],
            }).encode(),
        )
        result = search_films('test', 10)
        self.assertEqual(result[0]['film'], 'Dune')


class ParseAgeRatingTests(TestCase):
    """Tests for parse_age_rating helper function."""

    def test_parse_age_rating_with_valid_string(self):
        self.assertEqual(parse_age_rating('18+'), 18)

    def test_parse_age_rating_with_valid_number(self):
        self.assertEqual(parse_age_rating(16), 16)

    def test_parse_age_rating_with_none(self):
        self.assertIsNone(parse_age_rating(None))

    def test_parse_age_rating_with_empty_string(self):
        self.assertIsNone(parse_age_rating(''))

    def test_parse_age_rating_with_zero_string(self):
        self.assertIsNone(parse_age_rating('0'))

    def test_parse_age_rating_with_text_no_digits(self):
        self.assertIsNone(parse_age_rating('R'))

    def test_parse_age_rating_with_mixed_text_digits(self):
        self.assertEqual(parse_age_rating('NC-17'), 17)

    def test_parse_age_rating_with_two_digit_age(self):
        self.assertEqual(parse_age_rating('18+'), 18)

    def test_parse_age_rating_extracts_first_digits_only(self):
        self.assertEqual(parse_age_rating('12A'), 12)

    def test_parse_age_rating_with_false_value(self):
        self.assertIsNone(parse_age_rating(False))

    def test_parse_age_rating_with_zero(self):
        self.assertIsNone(parse_age_rating(0))


class StaffByProfessionTests(TestCase):
    """Tests for staff_by_profession helper function."""

    def test_staff_by_profession_filters_by_profession(self):
        staff = [
            {'professionKey': 'ACTOR', 'nameRu': 'Actor 1', 'nameEn': 'Actor 1 En'},
            {'professionKey': 'DIRECTOR', 'nameRu': 'Director 1', 'nameEn': 'Director 1 En'},
            {'professionKey': 'ACTOR', 'nameRu': 'Actor 2', 'nameEn': 'Actor 2 En'},
        ]
        result = staff_by_profession(staff, 'ACTOR', 10)
        self.assertEqual(len(result), 2)
        self.assertIn('Actor 1 / Actor 1 En', result)
        self.assertIn('Actor 2 / Actor 2 En', result)

    def test_staff_by_profession_respects_limit(self):
        staff = [
            {'professionKey': 'ACTOR', 'nameRu': f'Actor {i}', 'nameEn': f'Actor {i} En'}
            for i in range(20)
        ]
        result = staff_by_profession(staff, 'ACTOR', 5)
        self.assertEqual(len(result), 5)

    def test_staff_by_profession_with_empty_staff(self):
        result = staff_by_profession([], 'ACTOR', 10)
        self.assertEqual(result, [])

    def test_staff_by_profession_no_matching_profession(self):
        staff = [
            {'professionKey': 'ACTOR', 'nameRu': 'Actor 1', 'nameEn': 'Actor 1 En'},
        ]
        result = staff_by_profession(staff, 'DIRECTOR', 10)
        self.assertEqual(result, [])

    def test_staff_by_profession_with_zero_limit(self):
        staff = [
            {'professionKey': 'ACTOR', 'nameRu': 'Actor 1', 'nameEn': 'Actor 1 En'},
        ]
        result = staff_by_profession(staff, 'ACTOR', 0)
        self.assertEqual(result, [])

    def test_staff_by_profession_with_missing_names(self):
        staff = [
            {'professionKey': 'ACTOR', 'nameRu': None, 'nameEn': None},
            {'professionKey': 'ACTOR', 'nameRu': 'Actor 2', 'nameEn': None},
        ]
        result = staff_by_profession(staff, 'ACTOR', 10)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], '')
        self.assertEqual(result[1], 'Actor 2')

    def test_staff_by_profession_limit_greater_than_matches(self):
        staff = [
            {'professionKey': 'ACTOR', 'nameRu': 'Actor 1', 'nameEn': 'Actor 1 En'},
            {'professionKey': 'ACTOR', 'nameRu': 'Actor 2', 'nameEn': 'Actor 2 En'},
        ]
        result = staff_by_profession(staff, 'ACTOR', 100)
        self.assertEqual(len(result), 2)


class FormatPersonNameTests(TestCase):
    """Tests for format_person_name helper function."""

    def test_format_person_name_both_names_different(self):
        result = format_person_name('Иван', 'Ivan')
        self.assertEqual(result, 'Иван / Ivan')

    def test_format_person_name_both_names_same(self):
        result = format_person_name('Ivan', 'Ivan')
        self.assertEqual(result, 'Ivan')

    def test_format_person_name_only_ru(self):
        result = format_person_name('Иван', None)
        self.assertEqual(result, 'Иван')

    def test_format_person_name_only_en(self):
        result = format_person_name(None, 'Ivan')
        self.assertEqual(result, 'Ivan')

    def test_format_person_name_both_none(self):
        result = format_person_name(None, None)
        self.assertEqual(result, '')

    def test_format_person_name_empty_strings(self):
        result = format_person_name('', '')
        self.assertEqual(result, '')


class FetchFilmDetailsErrorTests(TestCase):
    """Additional error path tests for fetch_film_details."""

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_details_with_non_dict_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps('just a string').encode(),
        )

        with self.assertRaises(KinopoiskApiError):
            fetch_film_details(409424)

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_details_with_null_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps(None).encode(),
        )

        with self.assertRaises(KinopoiskApiError):
            fetch_film_details(409424)


class FetchFilmStaffEdgeCasesTests(TestCase):
    """Edge case tests for fetch_film_staff."""

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_staff_with_json_decode_error(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=b'{ invalid json',
        )

        result = fetch_film_staff(409424)
        self.assertEqual(result, [])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_staff_with_non_list_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps({'staff': 'not a list'}).encode(),
        )

        result = fetch_film_staff(409424)
        self.assertEqual(result, [])

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_staff_with_null_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps(None).encode(),
        )

        result = fetch_film_staff(409424)
        self.assertEqual(result, [])


class FetchFilmDistributionsEdgeCasesTests(TestCase):
    """Edge case tests for fetch_film_distributions."""

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_distributions_with_json_decode_error(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=b'{ invalid json',
        )

        result = fetch_film_distributions(409424)
        self.assertEqual(result, {})

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_distributions_with_non_dict_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps([1, 2, 3]).encode(),
        )

        result = fetch_film_distributions(409424)
        self.assertEqual(result, {})

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_distributions_with_null_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps(None).encode(),
        )

        result = fetch_film_distributions(409424)
        self.assertEqual(result, {})


class FetchFilmExternalSourcesEdgeCasesTests(TestCase):
    """Edge case tests for fetch_film_external_sources."""

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_external_sources_with_json_decode_error(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=b'{ invalid json',
        )

        result = fetch_film_external_sources(409424)
        self.assertEqual(result, {})

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_external_sources_with_non_dict_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps([1, 2, 3]).encode(),
        )

        result = fetch_film_external_sources(409424)
        self.assertEqual(result, {})

    @patch('todo.kinopoisk_api.kinopoisk_get')
    def test_fetch_film_external_sources_with_null_json(self, mock_get):
        mock_get.return_value = MagicMock(
            status_code=200,
            content=json.dumps(None).encode(),
        )

        result = fetch_film_external_sources(409424)
        self.assertEqual(result, {})

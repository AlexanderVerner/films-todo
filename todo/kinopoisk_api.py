import json
import logging
from datetime import datetime

import requests
from envjson import env_str

NO_POSTER = 'https://i.ibb.co/sbw3sB7/no-poster.png'

API_ERROR_MESSAGE = 'Please, check your configuration.'

logger = logging.getLogger(__name__)


class KinopoiskApiError(Exception):
    """Custom exception for Kinopoisk API errors."""
    pass


def _api_base_url():
    return env_str('KINOPOISK_API_URL').rstrip('/')


def _api_headers():
    return {'X-API-KEY': env_str('KINOPOISK_TOKEN')}


def kinopoisk_get(path, params=None):
    try:
        response = requests.get(
            url=f'{_api_base_url()}{path}',
            headers=_api_headers(),
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response
    except requests.RequestException as err:
        logger.error(
            'kinopoisk_api_error',
            extra={
                'url': f'{_api_base_url()}{path}',
                'params': params,
                'error': str(err),
                'status_code': getattr(err.response, 'status_code', None) if hasattr(err, 'response') else None,
            }
        )
        raise KinopoiskApiError(f"Failed to fetch from Kinopoisk API: {str(err)}") from err


def _decode_json_response(response, default_value=None, event_name=None):
    """Safely decode JSON response and handle errors with logging.
    
    Args:
        response: Response object with content to decode
        default_value: Value to return on JSON decode error (defaults to None)
        event_name: Event name for logging context
    
    Returns:
        Decoded JSON content or default_value on error
    """
    try:
        return json.loads(response.content)
    except json.JSONDecodeError as err:
        if event_name:
            logger.error(
                event_name,
                extra={'error': str(err)}
            )
        return default_value


def search_films(keyword, limit):
    """Search films by keyword.

    Returns:
        list: Mapped film results (may be empty).

    Raises:
        KinopoiskApiError: If the request fails or the response is malformed.
    """
    try:
        response = kinopoisk_get(
            '/api/v2.1/films/search-by-keyword',
            params={'keyword': keyword, 'page': 1},
        )
        payload = json.loads(response.content)
    except (KinopoiskApiError, json.JSONDecodeError) as err:
        logger.error(
            'search_films_error',
            extra={'keyword': keyword, 'error': str(err)}
        )
        raise KinopoiskApiError(API_ERROR_MESSAGE) from err
    if not isinstance(payload, dict):
        logger.error(
            'search_films_error',
            extra={'keyword': keyword, 'error': f'unexpected payload type {type(payload).__name__}'}
        )
        raise KinopoiskApiError(API_ERROR_MESSAGE)
    films = payload.get('films') or []
    content = []
    for item in films[: int(limit)]:
        description = item.get('description')
        year_raw = item.get('year')
        try:
            year = int(year_raw) if year_raw is not None else None
        except (TypeError, ValueError):
            year = None
        if description is None or not year:
            continue
        rating_raw = item.get('rating')
        try:
            rating_kp = float(rating_raw) if rating_raw not in (None, '') else None
        except (TypeError, ValueError):
            rating_kp = None
        content.append({
            'film': item.get('nameRu') or item.get('nameEn'),
            'year': year,
            'description': description,
            'poster': item.get('posterUrlPreview') or item.get('posterUrl') or NO_POSTER,
            'id_kinopoisk': item.get('filmId'),
            'rating_kp': rating_kp,
        })
    return content


def fetch_film_details(film_id):
    """Fetch film details by id.

    Returns:
        dict: Raw film details payload.

    Raises:
        KinopoiskApiError: If the request fails or the response is malformed.
    """
    try:
        response = kinopoisk_get(f'/api/v2.2/films/{film_id}')
    except KinopoiskApiError as err:
        logger.error(
            'fetch_film_details_error',
            extra={'film_id': film_id, 'error': str(err)}
        )
        raise KinopoiskApiError(API_ERROR_MESSAGE) from err
    content = _decode_json_response(
        response,
        default_value=None,
        event_name='fetch_film_details_error'
    )
    if not isinstance(content, dict):
        raise KinopoiskApiError(API_ERROR_MESSAGE)
    return content


def fetch_film_staff(film_id):
    """Fetch the staff list for a film.

    Staff is supplementary data, so failures degrade to an empty list
    instead of propagating: the caller always gets a list.
    """
    try:
        response = kinopoisk_get('/api/v1/staff', params={'filmId': film_id})
        staff = _decode_json_response(
            response,
            default_value=[],
            event_name='fetch_film_staff_error'
        )
        return staff if isinstance(staff, list) else []
    except KinopoiskApiError as err:
        logger.error(
            'fetch_film_staff_error',
            extra={'film_id': film_id, 'error': str(err)}
        )
        return []


def fetch_film_distributions(film_id):
    """Fetch distribution (premiere) data for a film.

    Distributions are supplementary data, so failures degrade to an empty
    dict instead of propagating: the caller always gets a dict.
    """
    try:
        response = kinopoisk_get(f'/api/v2.2/films/{film_id}/distributions')
        distributions = _decode_json_response(
            response,
            default_value={},
            event_name='fetch_film_distributions_error'
        )
        return distributions if isinstance(distributions, dict) else {}
    except KinopoiskApiError as err:
        logger.error(
            'fetch_film_distributions_error',
            extra={'film_id': film_id, 'error': str(err)}
        )
        return {}


def fetch_film_external_sources(film_id):
    """Fetch watchability sources for a film.

    External sources are supplementary data, so failures degrade to an
    empty dict instead of propagating: the caller always gets a dict.
    """
    try:
        response = kinopoisk_get(
            f'/api/v2.2/films/{film_id}/external_sources',
            params={'page': 1},
        )
        external_sources = _decode_json_response(
            response,
            default_value={},
            event_name='fetch_film_external_sources_error'
        )
        return external_sources if isinstance(external_sources, dict) else {}
    except KinopoiskApiError as err:
        logger.error(
            'fetch_film_external_sources_error',
            extra={'film_id': film_id, 'error': str(err)}
        )
        return {}


def premiere_dates_from_distributions(distributions):
    premiere_world = None
    premiere_russia = None
    for item in distributions.get('items') or []:
        date_str = item.get('date')
        if not date_str:
            continue
        try:
            premiere_date = datetime.fromisoformat(date_str).date()
        except ValueError:
            continue
        dist_type = item.get('type')
        country = (item.get('country') or {}).get('country')
        if dist_type == 'WORLD_PREMIER' and premiere_world is None:
            premiere_world = premiere_date
        if country == 'Россия' and dist_type in ('PREMIERE', 'COUNTRY_SPECIFIC'):
            if premiere_russia is None:
                premiere_russia = premiere_date
    return premiere_world, premiere_russia


def watchability_from_external_sources(external_sources):
    return [
        {'name': item.get('platform'), 'url': item.get('url')}
        for item in (external_sources.get('items') or [])
        if item.get('url')
    ]


def parse_age_rating(rating_age_limits):
    if not rating_age_limits:
        return None
    digits = ''.join(ch for ch in str(rating_age_limits) if ch.isdigit())
    return int(digits) if digits else None


def format_person_name(name_ru, name_en):
    if name_ru and name_en and name_ru != name_en:
        return f'{name_ru} / {name_en}'
    return name_ru or name_en or ''


def staff_by_profession(staff, profession_key, limit):
    return [
        format_person_name(person.get('nameRu'), person.get('nameEn'))
        for person in staff
        if person.get('professionKey') == profession_key
    ][:limit]


def build_film_detail(film_id):
    """Build a normalized film detail dict.

    Raises:
        KinopoiskApiError: If fetching the film details fails (propagated
            from `fetch_film_details`).
    """
    movie = fetch_film_details(film_id)

    staff = fetch_film_staff(film_id)
    distributions = fetch_film_distributions(film_id)
    external_sources = fetch_film_external_sources(film_id)
    premiere_world, premiere_russia = premiere_dates_from_distributions(distributions)

    actors = staff_by_profession(staff, 'ACTOR', 15)
    directors = staff_by_profession(staff, 'DIRECTOR', 5)

    return {
        'id_kinopoisk': movie.get('kinopoiskId'),
        'film': movie.get('nameRu'),
        'film_alternative': movie.get('nameEn') or movie.get('nameOriginal'),
        'type': movie.get('type'),
        'year': movie.get('year'),
        'slogan': movie.get('slogan'),
        'description': movie.get('description'),
        'genres': [genre.get('genre') for genre in (movie.get('genres') or [])],
        'age_rating': parse_age_rating(movie.get('ratingAgeLimits')),
        'countries': [country.get('country') for country in (movie.get('countries') or [])],
        'poster': movie.get('posterUrlPreview') or movie.get('posterUrl'),
        'rating_kp': movie.get('ratingKinopoisk'),
        'rating_imdb': movie.get('ratingImdb'),
        'votes_kp': movie.get('ratingKinopoiskVoteCount'),
        'votes_imdb': movie.get('ratingImdbVoteCount'),
        'premiere_world': premiere_world,
        'premiere_russia': premiere_russia,
        'watchability': watchability_from_external_sources(external_sources),
        'actors': actors,
        'directors': directors,
    }

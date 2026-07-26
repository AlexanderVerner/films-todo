import json
from datetime import datetime

import requests
from envjson import env_str

NO_POSTER = 'https://i.ibb.co/sbw3sB7/no-poster.png'


def _api_base_url():
    return env_str('KINOPOISK_API_URL').rstrip('/')


def _api_headers():
    return {'X-API-KEY': env_str('KINOPOISK_TOKEN')}


def kinopoisk_get(path, params=None):
    response = requests.get(
        url=f'{_api_base_url()}{path}',
        headers=_api_headers(),
        params=params,
        timeout=30,
    )
    return response


def search_films(keyword, limit):
    response = kinopoisk_get(
        '/api/v2.1/films/search-by-keyword',
        params={'keyword': keyword, 'page': 1},
    )
    if response.status_code != 200:
        return {'message': 'Please, check your configuration.'}

    films = json.loads(response.content).get('films') or []
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
    response = kinopoisk_get(f'/api/v2.2/films/{film_id}')
    if response.status_code != 200:
        return {'message': 'Please, check your configuration.'}
    return json.loads(response.content)


def fetch_film_staff(film_id):
    response = kinopoisk_get('/api/v1/staff', params={'filmId': film_id})
    if response.status_code != 200:
        return []
    return json.loads(response.content)


def fetch_film_distributions(film_id):
    response = kinopoisk_get(f'/api/v2.2/films/{film_id}/distributions')
    if response.status_code != 200:
        return {}
    return json.loads(response.content)


def fetch_film_external_sources(film_id):
    response = kinopoisk_get(
        f'/api/v2.2/films/{film_id}/external_sources',
        params={'page': 1},
    )
    if response.status_code != 200:
        return {}
    return json.loads(response.content)


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
    movie = fetch_film_details(film_id)
    if 'message' in movie:
        return movie

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

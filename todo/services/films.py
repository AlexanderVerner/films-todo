import logging
from typing import Protocol

from envjson import env_str

from todo.kinopoisk_api import search_films, build_film_detail, KinopoiskApiError

logger = logging.getLogger(__name__)


class FilmsService:
    """Service for searching and fetching film details from Kinopoisk API."""

    @staticmethod
    def search_films(keyword: str, limit: int | None = None) -> list[dict]:
        """Search films by keyword.
        
        Args:
            keyword: Search query
            limit: Maximum number of results to return. If None, uses MAX_COUNT_MOVIE_PER_REQUEST from env
            
        Returns:
            List of film dictionaries with basic info (title, year, description, poster, rating, id_kinopoisk)
            
        Raises:
            KinopoiskApiError: If the API request fails or returns malformed data
        """
        if limit is None:
            limit = int(env_str('MAX_COUNT_MOVIE_PER_REQUEST'))
        
        try:
            logger.debug('search_films_request', extra={'keyword': keyword, 'limit': limit})
            films = search_films(keyword, limit)
            logger.info('search_films_success', extra={'keyword': keyword, 'count': len(films)})
            return films
        except KinopoiskApiError as err:
            logger.error('search_films_failed', extra={'keyword': keyword, 'error': str(err)})
            raise

    @staticmethod
    def get_film_detail(film_id: int) -> dict:
        """Fetch detailed information about a film.
        
        Args:
            film_id: Kinopoisk film ID
            
        Returns:
            Dictionary with complete film details:
            - id_kinopoisk, film, film_alternative, type, year
            - slogan, description, genres, age_rating, countries
            - poster, rating_kp, rating_imdb, votes_kp, votes_imdb
            - premiere_world, premiere_russia, watchability, actors, directors
            
        Raises:
            KinopoiskApiError: If the API request fails or returns malformed data
        """
        try:
            logger.debug('get_film_detail_request', extra={'film_id': film_id})
            film_detail = build_film_detail(film_id)
            logger.info('get_film_detail_success', extra={'film_id': film_id, 'title': film_detail.get('film')})
            return film_detail
        except KinopoiskApiError as err:
            logger.error('get_film_detail_failed', extra={'film_id': film_id, 'error': str(err)})
            raise

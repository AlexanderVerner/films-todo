"""
Movie API response mappers and serializers.

Converts Kinopoisk API detail responses to Movie model field mappings.
"""


def movie_defaults_from_detail(detail: dict) -> dict:
    """
    Map API detail response to Movie model defaults.
    
    Takes a dictionary from the Kinopoisk API and returns a dict suitable
    for Movie.objects.update_or_create(defaults={...})
    
    Args:
        detail: API detail response dictionary with keys like 'film', 'year', etc.
    
    Returns:
        Dictionary with Movie model field names as keys, ready for update_or_create.
    """
    return {
        'title': detail.get('film'),
        'title_alternative': detail.get('film_alternative'),
        'description': detail.get('description'),
        'year': detail.get('year'),
        'poster': detail.get('poster'),
        'rating_kinopoisk': detail.get('rating_kp'),
        'type': detail.get('type'),
        'slogan': detail.get('slogan'),
        'genres': detail.get('genres'),
        'age_rating': detail.get('age_rating'),
        'countries': detail.get('countries'),
        'rating_imdb': detail.get('rating_imdb'),
        'kinopoisk_votes': detail.get('votes_kp'),
        'imdb_votes': detail.get('votes_imdb'),
        'premiere_world': detail.get('premiere_world'),
        'premiere_russia': detail.get('premiere_russia'),
        'watchability': detail.get('watchability'),
        'actors': detail.get('actors'),
        'directors': detail.get('directors'),
    }

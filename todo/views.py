import json
import requests

from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from envjson import env_str
from todo.forms import SearchForm
from todo.models import Note, Movie


def get_note_list(self):
    try:
        notes_list = Note.objects.all()
    except Note.DoesNotExist:
        return None
    else:
        return notes_list


def get_preview_content(request, field, sort_field):
    search_text = request.POST.get('id_kinopoisk', None)
    token = env_str('KINOPOISK_TOKEN')
    host_api = env_str('KINOPOISK_API_URL')
    limit = env_str('MAX_COUNT_MOVIE_PER_REQUEST')
    if search_text:
        response = requests.get(
            url=f'{host_api}?token={token}&search={search_text}&field={field}'
                f'&sortField={sort_field}&sortType=-1&limit={limit}'
        )
        if response.status_code == 200:
            docs = json.loads(response.content).get('docs')
            content = []
            for item in docs:
                description = item.get('description', None)
                if description is not None:
                    info = {'film': item.get('name'),
                            'year': item.get('year'),
                            'description': description,
                            'poster': get_nested_object(item, 'poster', 'url',
                                                        'https://i.ibb.co/sbw3sB7/no-poster.png'),
                            'id_kinopoisk': item.get('id'),
                            'rating_kp': get_nested_object(item, 'rating', 'kp')}
                    content.append(info)
            return content
        else:
            return {'message': 'Please, check your configuration.'}


def get_detail_film(id_kinopoisk):
    token = env_str('KINOPOISK_TOKEN')
    host_api = env_str('KINOPOISK_API_URL')
    response = requests.get(
        url=f'{host_api}?token={token}&search={id_kinopoisk}&field=id')
    if response.status_code == 200:
        movie = json.loads(response.content)
        persons = movie.get('persons')
        actors = [{item.get('name'): item.get('enName', None)}
                  for item in persons if item['enProfession'] == 'actor'][:15]
        directors = [{item.get('name'): item.get('enName', None)}
                     for item in persons if item['enProfession'] == 'director'][:5]
        content = {'id_kinopoisk': movie.get('id'),
                   'film': movie.get('name'),
                   'film_alternative': movie.get('alternativeName', None),
                   'type': movie.get('type'),
                   'year': movie.get('year', None),
                   'slogan': movie.get('slogan', None),
                   'description': movie.get('description'),
                   'genres': [item.get('name') for item in movie.get('genres')],
                   'age_rating': movie.get('ageRating'),
                   'countries': [item.get('name') for item in movie.get('countries')],
                   'poster': get_nested_object(movie, 'poster', 'url'),
                   'rating_kp': get_nested_object(movie, 'rating', 'kp'),
                   'rating_imdb': get_nested_object(movie, 'rating', 'imdb'),
                   'votes_kp': get_nested_object(movie, 'votes', 'kp'),
                   'votes_imdb': get_nested_object(movie, 'votes', 'imdb'),
                   'premiere_world': get_date_from_iso(movie, 'premiere', 'world'),
                   'premiere_russia': get_date_from_iso(movie, 'premiere', 'russia'),
                   'watchability': get_nested_object(movie, 'watchability', 'items'),
                   'actors': actors,
                   'directors': directors
                   }
        return content
    else:
        return {'message': 'Please, check your configuration.'}


def get_nested_object(content, first_level, second_level, if_missing=None):
    item = content.get(first_level)
    return item.get(second_level) if item else if_missing


def get_date_from_iso(content, first_level, second_level):
    try:
        return datetime.fromisoformat((content.get(first_level).get(second_level))[:-1]).date()
    except TypeError:
        return None


class IndexView(TemplateView):
    template_name = 'todo/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'todo/index.html', self.get_context())

    def get_context(self):
        notes = get_note_list(self)
        form = SearchForm()
        context = {'note_list': notes,
                   'form': form}
        return context


class PreView(TemplateView):
    template_name = 'todo/preview.html'

    def post(self, request, *args, **kwargs):
        content = get_preview_content(request, field='name', sort_field='votes.imdb')
        if 'message' in content:
            return render(request, 'todo/error.html', content)
        else:
            return render(request, 'todo/preview.html', {'movies': content})


class DetailView(TemplateView):
    template_name = 'todo/detail.html'

    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs.get('note_id'))
        return render(request, 'todo/detail.html', {'note': note})


class SaveView(View):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=1)
        content = get_detail_film(kwargs.get('id_kinopoisk'))
        entry_film, _ = Movie.objects.update_or_create(id_kinopoisk=content.get('id_kinopoisk'),
                                                       defaults={
                                                           'title': content.get('film'),
                                                           'title_alternative': content.get('film_alternative'),
                                                           'description': content.get('description'),
                                                           'year': content.get('year'),
                                                           'poster': content.get('poster'),
                                                           'rating_kinopoisk': content.get('rating_kp'),
                                                           'type': content.get('type'),
                                                           'slogan': content.get('slogan'),
                                                           'genres': content.get('genres'),
                                                           'age_rating': content.get('age_rating'),
                                                           'countries': content.get('countries'),
                                                           'rating_imdb': content.get('rating_imdb'),
                                                           'kinopoisk_votes': content.get('votes_kp'),
                                                           'imdb_votes': content.get('votes_imdb'),
                                                           'premiere_world': content.get('premiere_world'),
                                                           'premiere_russia': content.get('premiere_russia'),
                                                           'watchability': content.get('watchability'),
                                                           'actors': content.get('actors'),
                                                           'directors': content.get('directors')
                                                       })
        Note.objects.update_or_create(user=user, movie=entry_film)
        return redirect('todo:index')


class DeleteView(View):

    def post(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs.get('note_id'))
        if note:
            note.delete()
        return redirect('todo:index')

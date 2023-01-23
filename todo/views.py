from datetime import datetime

import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from envjson import env_str
from todo.models import Note, Movie
from todo.forms import SearchForm
from django.contrib.auth.models import User


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
            docs = response.json().get('docs')
            content = []
            for item in docs:
                film = item.get('name')
                id_kinopoisk = item.get('id')
                description = item.get('description')
                year = item.get('year')
                poster = item.get('poster')
                poster = poster.get('url') if poster else None
                rating_kp = item.get('rating').get('kp')
                if description is not None:
                    info = {'film': film,
                            'year': year,
                            'description': description,
                            'poster': poster,
                            'id_kinopoisk': id_kinopoisk,
                            'rating_kp': rating_kp}
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
        movie = response.json()
        persons = movie.get('persons')
        actors = [{item.get('name'): item.get('enName')}
                  for item in persons if item['enProfession'] == 'actor'][:15]
        directors = [{item.get('name'): item.get('enName')}
                     for item in persons if item['enProfession'] == 'director'][:5]
        content = {'id_kinopoisk': movie.get('id'),
                   'film': movie.get('name'),
                   'film_alternative': movie.get('alternativeName'),
                   'type': movie.get('type'),
                   'year': movie.get('year'),
                   'slogan': movie.get('slogan'),
                   'description': movie.get('description'),
                   'genres': [item.get('name') for item in movie.get('genres')],
                   'age_rating': movie.get('ageRating'),
                   'countries': [item.get('name') for item in movie.get('countries')],
                   'poster': movie.get('poster').get('url'),
                   'rating_kp': movie.get('rating').get('kp'),
                   'rating_imdb': movie.get('rating').get('imdb'),
                   'votes_kp': movie.get('votes').get('kp'),
                   'votes_imdb': movie.get('votes').get('imdb'),
                   'premiere_world': datetime.fromisoformat((movie.get('premiere').get('world'))[:-1]).date(),
                   'premiere_russia': datetime.fromisoformat((movie.get('premiere').get('russia'))[:-1]).date(),
                   'watchability': movie.get('watchability').get('items'),
                   'actors': actors,
                   'directors': directors
                   }
        return content
    else:
        return {'message': 'Please, check your configuration.'}


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

import requests
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
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


def get_film_content(request, field):
    user = get_object_or_404(User, pk=1)
    search_text = request.POST.get('id_kinopoisk', None)
    token = env_str('KINOPOISK_TOKEN')
    host_api = env_str('KINOPOISK_API_URL')
    if search_text:
        response = requests.get(
            url=f'{host_api}?token={token}&search={search_text}&field={field}'
        )
        if response.status_code == 200:
            film = response.json().get('name')
            id_kinopoisk = response.json().get('id')
            description = response.json().get('description')
            year = response.json().get('year')
            poster = response.json().get('poster').get('url')
            content = {'user': user,
                       'film': film,
                       'year': year,
                       'description': description,
                       'poster': poster,
                       'id_kinopoisk': id_kinopoisk}
            return content
        elif response.status_code == 404:
            return {'message': 'Movie not found. Please, check input value.'}
        else:
            return {'message': 'Please, check your configuration.'}


class IndexView(TemplateView):
    template_name = 'todo/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'todo/index.html', self.get_context())

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=1)
        entry_film, _ = Movie.objects.update_or_create(title=request.session['title'],
                                                       id_kinopoisk=request.session['id_kinopoisk'],
                                                       description=request.session['description'],
                                                       year=request.session['year'],
                                                       poster=request.session['poster'])
        Note.objects.update_or_create(user=user, movie=entry_film)
        return render(request, 'todo/index.html', self.get_context())

    def get_context(self):
        notes = get_note_list(self)
        form = SearchForm()
        context = {'note_list': notes,
                   'form': form}
        return context


class NoteView(TemplateView):
    template_name = 'todo/note.html'

    def post(self, request, *args, **kwargs):
        content = get_film_content(request, field="id")
        if 'message' in content:
            return render(request, 'todo/error.html', content)
        else:
            request.session['id_kinopoisk'] = content['id_kinopoisk']
            request.session['title'] = content['film']
            request.session['description'] = content['description']
            request.session['year'] = content['year']
            request.session['poster'] = content['poster']
            return render(request, 'todo/note.html', content)

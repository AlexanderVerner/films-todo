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


def get_film_content(request, field, sort_field):
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
        content = get_film_content(request, field='name', sort_field='votes.imdb')
        if 'message' in content:
            return render(request, 'todo/error.html', content)
        else:
            request.session['content'] = content
            return render(request, 'todo/preview.html', {'movies': content})


class DetailView(TemplateView):
    template_name = 'todo/detail.html'

    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs.get('note_id'))
        return render(request, 'todo/detail.html', {'note': note})


class SaveView(View):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=1)
        movies = request.session['content']
        content = next((item for item in movies if item['id_kinopoisk'] == kwargs.get('id_kinopoisk')), None)
        entry_film, _ = Movie.objects.update_or_create(title=content.get('film'),
                                                       id_kinopoisk=content.get('id_kinopoisk'),
                                                       description=content.get('description'),
                                                       year=content.get('year'),
                                                       poster=content.get('poster'),
                                                       rating_kinopoisk=content.get('rating_kp'))
        Note.objects.update_or_create(user=user, movie=entry_film)

        return redirect('todo:index')


class DeleteView(View):

    def post(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs.get('note_id'))
        if note:
            note.delete()
        return redirect('todo:index')

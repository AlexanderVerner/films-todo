from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from todo.forms import SearchForm
from todo.kinopoisk_api import build_film_detail, search_films
from todo.models import Note, Movie


def get_note_list(self):
    try:
        notes_list = Note.objects.all()
    except Note.DoesNotExist:
        return None
    else:
        return notes_list


def get_preview_content(request):
    from envjson import env_str

    search_text = request.POST.get('title', None)
    limit = env_str('MAX_COUNT_MOVIE_PER_REQUEST')
    if not search_text:
        return []
    return search_films(search_text, limit)


def get_detail_film(id_kinopoisk):
    return build_film_detail(id_kinopoisk)


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
        content = get_preview_content(request)
        if isinstance(content, dict) and 'message' in content:
            return HttpResponse(
                render(request, 'todo/error.html', content).content,
                status=503,
                content_type='text/html'
            )
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
        if 'message' in content:
            return HttpResponse(
                render(request, 'todo/error.html', content).content,
                status=503,
                content_type='text/html'
            )
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

# class SeenView(View):
#
#     def post(self, request, *args, **kwargs):
#         note = get_object_or_404(Note, pk=kwargs.get('note_id'))
#         review = kwargs.get('review')
#         if note:

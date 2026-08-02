import logging
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from django.http import HttpResponse
from todo.forms import SearchForm
from todo.kinopoisk_api import build_film_detail, search_films, KinopoiskApiError
from todo.models import Note, Movie
from todo.serializers import movie_defaults_from_detail

logger = logging.getLogger(__name__)


def get_note_list(user):
    """Fetch user's notes with related movies to avoid N+1 queries."""
    return Note.objects.select_related('movie').filter(user=user)


def get_preview_content(request):
    from envjson import env_str

    search_text = request.POST.get('title', None)
    limit = env_str('MAX_COUNT_MOVIE_PER_REQUEST')
    if not search_text:
        return []
    return search_films(search_text, limit)


def get_detail_film(id_kinopoisk):
    return build_film_detail(id_kinopoisk)


def render_api_error(request):
    return HttpResponse(
        render(request, 'todo/error.html', {'message': 'Please, check your configuration.'}).content,
        status=503,
        content_type='text/html'
    )


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'todo/index.html'
    login_url = 'admin:login'

    def get(self, request, *args, **kwargs):
        return render(request, 'todo/index.html', self.get_context(request))

    def get_context(self, request):
        notes = get_note_list(request.user)
        form = SearchForm()
        context = {'note_list': notes,
                   'form': form}
        return context


class PreView(LoginRequiredMixin, TemplateView):
    template_name = 'todo/preview.html'
    login_url = 'admin:login'

    def post(self, request, *args, **kwargs):
        try:
            content = get_preview_content(request)
            return render(request, 'todo/preview.html', {'movies': content})
        except KinopoiskApiError as err:
            logger.warning('preview_error', extra={'message': str(err)})
            return render_api_error(request)
        except Exception as err:
            logger.error('preview_exception', extra={'error': str(err)})
            raise


class DetailView(LoginRequiredMixin, TemplateView):
    template_name = 'todo/detail.html'
    login_url = 'admin:login'

    def get(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs.get('note_id'), user=request.user)
        return render(request, 'todo/detail.html', {'note': note})


class SaveView(LoginRequiredMixin, View):
    login_url = 'admin:login'

    def post(self, request, *args, **kwargs):
        try:
            content = get_detail_film(kwargs.get('id_kinopoisk'))
            entry_film, _ = Movie.objects.update_or_create(
                id_kinopoisk=content.get('id_kinopoisk'),
                defaults=movie_defaults_from_detail(content)
            )
            Note.objects.update_or_create(user=request.user, movie=entry_film)
            logger.info('film_saved', extra={'id_kinopoisk': content.get('id_kinopoisk'), 'title': content.get('film')})
            return redirect('todo:index')
        except KinopoiskApiError as err:
            logger.warning('save_error', extra={'id_kinopoisk': kwargs.get('id_kinopoisk'), 'message': str(err)})
            return render_api_error(request)
        except Exception as err:
            logger.error('save_exception', extra={'error': str(err), 'id_kinopoisk': kwargs.get('id_kinopoisk')})
            raise


class DeleteView(LoginRequiredMixin, View):
    login_url = 'admin:login'

    def post(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs.get('note_id'), user=request.user)
        if note:
            note.delete()
        return redirect('todo:index')

# class SeenView(View):
#
#     def post(self, request, *args, **kwargs):
#         note = get_object_or_404(Note, pk=kwargs.get('note_id'))
#         review = kwargs.get('review')
#         if note:

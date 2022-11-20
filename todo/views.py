import requests
from django.shortcuts import render
from envjson import env_str


def index(request):
    return render(request, 'todo/index.html')


def get_film_content(request, input_name, field):
    search_text = request.POST.get(input_name, False)
    token = env_str('KINOPOISK_TOKEN')
    host_api = env_str('KINOPOISK_API_URL')
    response = requests.get(
        url=f'{host_api}?token={token}&search={search_text}&field={field}'
    )
    film = response.json().get('name')
    id_kinopoisk = response.json().get('id')
    description = response.json().get('description')
    year = response.json().get('year')
    poster = response.json().get('poster').get('url')
    content = {'film': film,
               'year': year,
               'description': description,
               'poster': poster,
               'id_kinopoisk': id_kinopoisk}
    return content
    
    
def note_by_id(request):
    content = get_film_content(request, input_name="id_kinopoisk", field="id")
    return render(request, f'todo/note.html', content)

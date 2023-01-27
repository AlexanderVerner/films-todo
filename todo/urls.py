from django.urls import path
from todo.views import IndexView, PreView, SaveView, DetailView, DeleteView

app_name = 'todo'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('preview', PreView.as_view(), name='preview'),
    path('preview/<int:id_kinopoisk>', SaveView.as_view(), name='save'),
    path('detail/<int:note_id>', DetailView.as_view(), name='detail'),
    path('detail/<int:note_id>/delete', DeleteView.as_view(), name='delete')
]

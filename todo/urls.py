from django.urls import path
from todo.views import IndexView, NoteView, DetailView

app_name = 'todo'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('preview', NoteView.as_view(), name='preview_note'),
    path('detail/<int:note_id>', DetailView.as_view(), name='detail')
]

from django.urls import path
from todo.views import IndexView, NoteView

app_name = 'todo'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('note', NoteView.as_view(), name='preview_note'),
]

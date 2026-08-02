import pytest
from datetime import date
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from todo.models import Movie, Note
from todo.services.notes import NoteService
from todo.services.films import FilmsService
from todo.kinopoisk_api import KinopoiskApiError


@pytest.mark.django_db
class TestNoteService(TestCase):
    """Tests for NoteService."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass')
        self.movie = Movie.objects.create(
            id_kinopoisk=1,
            title='Test Movie',
            poster='https://example.com/poster.jpg',
        )

    def test_get_note_list_returns_all_user_notes(self):
        """Test getting all notes for a user."""
        note1 = Note.objects.create(user=self.user, movie=self.movie)
        movie2 = Movie.objects.create(
            id_kinopoisk=2,
            title='Another Movie',
            poster='https://example.com/poster2.jpg',
        )
        note2 = Note.objects.create(user=self.user, movie=movie2)
        
        notes = NoteService.get_note_list(self.user)
        
        assert len(notes) == 2
        assert note1 in notes
        assert note2 in notes

    def test_get_note_list_filters_by_user(self):
        """Test that get_note_list only returns notes for specified user."""
        note1 = Note.objects.create(user=self.user, movie=self.movie)
        note2 = Note.objects.create(user=self.other_user, movie=self.movie)
        
        notes = NoteService.get_note_list(self.user)
        
        assert len(notes) == 1
        assert note1 in notes
        assert note2 not in notes

    def test_get_note_returns_existing_note(self):
        """Test retrieving a specific note."""
        note = Note.objects.create(user=self.user, movie=self.movie)
        
        retrieved_note = NoteService.get_note(note.id, self.user)
        
        assert retrieved_note.id == note.id
        assert retrieved_note.user_id == self.user.id
        assert retrieved_note.movie_id == self.movie.id

    def test_get_note_raises_404_for_nonexistent_note(self):
        """Test that Http404 is raised for non-existent note."""
        with pytest.raises(Http404):
            NoteService.get_note(999, self.user)

    def test_get_note_raises_404_if_note_belongs_to_other_user(self):
        """Test that Http404 is raised if note belongs to different user."""
        note = Note.objects.create(user=self.other_user, movie=self.movie)
        
        with pytest.raises(Http404):
            NoteService.get_note(note.id, self.user)

    def test_create_note_creates_new_note(self):
        """Test creating a new note."""
        note = NoteService.create_note(self.user, self.movie)
        
        assert note.user_id == self.user.id
        assert note.movie_id == self.movie.id
        
        # Verify it was saved to database
        assert Note.objects.filter(id=note.id).exists()

    def test_create_note_returns_existing_note_if_already_exists(self):
        """Test that create_note returns existing note instead of creating duplicate."""
        existing_note = Note.objects.create(user=self.user, movie=self.movie)
        
        returned_note = NoteService.create_note(self.user, self.movie)
        
        assert returned_note.id == existing_note.id
        # Verify no duplicate was created
        assert Note.objects.filter(user=self.user, movie=self.movie).count() == 1

    def test_delete_note_removes_note(self):
        """Test deleting a note."""
        note = Note.objects.create(user=self.user, movie=self.movie)
        
        NoteService.delete_note(note.id, self.user)
        
        assert not Note.objects.filter(id=note.id).exists()

    def test_delete_note_raises_404_for_nonexistent_note(self):
        """Test that Http404 is raised when deleting non-existent note."""
        with pytest.raises(Http404):
            NoteService.delete_note(999, self.user)

    def test_delete_note_raises_404_if_note_belongs_to_other_user(self):
        """Test that Http404 is raised when deleting note of another user."""
        note = Note.objects.create(user=self.other_user, movie=self.movie)
        
        with pytest.raises(Http404):
            NoteService.delete_note(note.id, self.user)


class TestFilmsService:
    """Tests for FilmsService."""

    @patch('todo.services.films.search_films')
    @patch('todo.services.films.env_str')
    def test_search_films_returns_list_of_films(self, mock_env_str, mock_search_films):
        """Test searching for films."""
        mock_env_str.return_value = '10'
        films_data = [
            {
                'film': 'Test Film',
                'year': 2024,
                'description': 'A test film',
                'poster': 'https://example.com/poster.jpg',
                'id_kinopoisk': 1,
                'rating_kp': 8.5,
            }
        ]
        mock_search_films.return_value = films_data
        
        result = FilmsService.search_films('test', limit=10)
        
        assert len(result) == 1
        assert result[0]['film'] == 'Test Film'
        mock_search_films.assert_called_once_with('test', 10)

    @patch('todo.services.films.search_films')
    @patch('todo.services.films.env_str')
    def test_search_films_uses_env_limit_if_not_provided(self, mock_env_str, mock_search_films):
        """Test that search_films uses environment limit if not specified."""
        mock_env_str.return_value = '5'
        mock_search_films.return_value = []
        
        FilmsService.search_films('test')
        
        mock_search_films.assert_called_once_with('test', 5)

    @patch('todo.services.films.search_films')
    @patch('todo.services.films.env_str')
    def test_search_films_raises_on_api_error(self, mock_env_str, mock_search_films):
        """Test that search_films propagates KinopoiskApiError."""
        mock_env_str.return_value = '10'
        mock_search_films.side_effect = KinopoiskApiError('API error')
        
        with pytest.raises(KinopoiskApiError):
            FilmsService.search_films('test')

    @patch('todo.services.films.build_film_detail')
    def test_get_film_detail_returns_film_data(self, mock_build_film_detail):
        """Test fetching film details."""
        film_data = {
            'id_kinopoisk': 1,
            'film': 'Test Film',
            'year': 2024,
            'description': 'A test film',
            'poster': 'https://example.com/poster.jpg',
            'rating_kp': 8.5,
            'actors': ['Actor 1', 'Actor 2'],
            'directors': ['Director 1'],
            'genres': ['Drama', 'Thriller'],
        }
        mock_build_film_detail.return_value = film_data
        
        result = FilmsService.get_film_detail(1)
        
        assert result['film'] == 'Test Film'
        assert result['id_kinopoisk'] == 1
        mock_build_film_detail.assert_called_once_with(1)

    @patch('todo.services.films.build_film_detail')
    def test_get_film_detail_raises_on_api_error(self, mock_build_film_detail):
        """Test that get_film_detail propagates KinopoiskApiError."""
        mock_build_film_detail.side_effect = KinopoiskApiError('API error')
        
        with pytest.raises(KinopoiskApiError):
            FilmsService.get_film_detail(1)

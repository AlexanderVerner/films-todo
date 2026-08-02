from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from todo.models import Note, Movie


DUNE_DETAIL = {
    'id_kinopoisk': 409424,
    'film': 'Дюна',
    'film_alternative': 'Dune',
    'type': 'FILM',
    'year': 2021,
    'slogan': None,
    'description': 'Test description',
    'genres': ['фантастика'],
    'age_rating': 12,
    'countries': ['США'],
    'poster': 'https://example.com/poster.jpg',
    'rating_kp': 7.9,
    'rating_imdb': 8.0,
    'votes_kp': 100,
    'votes_imdb': 200,
    'premiere_world': None,
    'premiere_russia': None,
    'watchability': [],
    'actors': [],
    'directors': [],
}


class AuthenticationTests(TestCase):

    def test_index_requires_login(self):
        """IndexView should redirect unauthenticated users to login"""
        r = self.client.get(reverse('todo:index'))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.url.startswith('/admin/login'))

    def test_preview_requires_login(self):
        """PreView should redirect unauthenticated users to login"""
        r = self.client.post(reverse('todo:preview'), {'title': 'dune'})
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.url.startswith('/admin/login'))

    def test_save_requires_login(self):
        """SaveView should redirect unauthenticated users to login"""
        r = self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.url.startswith('/admin/login'))

    def test_detail_requires_login(self):
        """DetailView should redirect unauthenticated users to login"""
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': 1}))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.url.startswith('/admin/login'))

    def test_delete_requires_login(self):
        """DeleteView should redirect unauthenticated users to login"""
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': 1}))
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.url.startswith('/admin/login'))


class NoteOwnershipTests(TestCase):

    def setUp(self):
        """Create two users and their notes"""
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        self.movie1 = Movie.objects.create(
            id_kinopoisk=409424,
            title='Дюна',
            poster='https://example.com/dune.jpg'
        )
        self.movie2 = Movie.objects.create(
            id_kinopoisk=123456,
            title='Интерстеллар',
            poster='https://example.com/interstellar.jpg'
        )

        self.note1_user1 = Note.objects.create(user=self.user1, movie=self.movie1)
        self.note1_user2 = Note.objects.create(user=self.user2, movie=self.movie2)

    def test_index_shows_only_own_notes(self):
        """IndexView should show only the logged-in user's notes"""
        self.client.login(username='user1', password='pass123')
        r = self.client.get(reverse('todo:index'))
        
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.note1_user1, r.context['note_list'])
        self.assertNotIn(self.note1_user2, r.context['note_list'])

    def test_detail_own_note_allowed(self):
        """DetailView should allow viewing own note"""
        self.client.login(username='user1', password='pass123')
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': self.note1_user1.id}))
        
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.context['note'], self.note1_user1)

    def test_detail_others_note_forbidden(self):
        """DetailView should return 404 when accessing another user's note"""
        self.client.login(username='user1', password='pass123')
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': self.note1_user2.id}))
        
        self.assertEqual(r.status_code, 404)

    def test_delete_own_note_allowed(self):
        """DeleteView should allow deleting own note"""
        self.client.login(username='user1', password='pass123')
        note_id = self.note1_user1.id
        
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': note_id}))
        
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Note.objects.filter(id=note_id).exists())

    def test_delete_others_note_forbidden(self):
        """DeleteView should return 404 when trying to delete another user's note"""
        self.client.login(username='user1', password='pass123')
        note_id = self.note1_user2.id
        
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': note_id}))
        
        self.assertEqual(r.status_code, 404)
        self.assertTrue(Note.objects.filter(id=note_id).exists())

    @patch('todo.views.build_film_detail', return_value=DUNE_DETAIL)
    def test_save_creates_note_for_current_user(self, mock_detail):
        """SaveView should create note for the current authenticated user"""
        self.client.login(username='user1', password='pass123')
        
        r = self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        
        self.assertEqual(r.status_code, 302)
        note = Note.objects.get(user=self.user1, movie__id_kinopoisk=409424)
        self.assertEqual(note.user, self.user1)

    @patch('todo.views.build_film_detail', return_value=DUNE_DETAIL)
    def test_save_different_users_different_notes(self, mock_detail):
        """SaveView should create separate notes for different users saving same movie"""
        self.client.login(username='user1', password='pass123')
        self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        
        self.client.logout()
        self.client.login(username='user2', password='pass123')
        self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        
        notes = Note.objects.filter(movie__id_kinopoisk=409424)
        self.assertEqual(notes.count(), 2)
        self.assertEqual(notes.filter(user=self.user1).count(), 1)
        self.assertEqual(notes.filter(user=self.user2).count(), 1)

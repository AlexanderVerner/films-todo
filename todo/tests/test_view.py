from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from todo.kinopoisk_api import KinopoiskApiError
from todo.models import Movie, Note


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

API_ERROR = KinopoiskApiError('Please, check your configuration.')


class IndexViewTests(TestCase):

    def test_get_index_view(self):
        r = self.client.get(reverse('todo:index'))
        self.assertEqual(r.status_code, 200)


class PreViewTests(TestCase):

    def test_get_preview_view(self):
        r = self.client.get(reverse('todo:preview'))
        self.assertEqual(r.status_code, 200)

    @patch('todo.views.get_preview_content')
    def test_preview_search_success(self, mock_search):
        mock_search.return_value = [
            {'id_kinopoisk': 409424, 'film': 'Дюна'}
        ]
        r = self.client.post(reverse('todo:preview'), {'title': 'dune'})
        self.assertEqual(r.status_code, 200)

    @patch('todo.views.get_preview_content')
    def test_preview_empty_query_returns_empty_list(self, mock_search):
        """PreView.post with empty title should return empty list"""
        mock_search.return_value = []
        r = self.client.post(reverse('todo:preview'), {'title': ''})
        self.assertEqual(r.status_code, 200)

    @patch('todo.views.get_preview_content')
    def test_preview_api_error_returns_503(self, mock_search):
        """PreView.post should return 503 when the API layer raises"""
        mock_search.side_effect = API_ERROR
        r = self.client.post(reverse('todo:preview'), {'title': 'dune'})
        self.assertEqual(r.status_code, 503)
        self.assertIn(b'Please, check your configuration', r.content)


class SaveViewTests(TestCase):

    def setUp(self):
        """Create User with pk=1 for testing SaveView"""
        User.objects.create_user(username='testuser', password='testpass123')

    @patch('todo.views.build_film_detail', return_value=DUNE_DETAIL)
    def test_post_save_movie(self, _mock_detail):
        """SaveView.post should save movie and redirect on success"""
        r = self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        movie = Movie.objects.get(id_kinopoisk=409424)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(movie.title, 'Дюна')

    @patch('todo.views.get_detail_film')
    def test_save_api_error_returns_503(self, mock_detail):
        """SaveView.post should return 503 when the API layer raises"""
        mock_detail.side_effect = API_ERROR
        r = self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        self.assertEqual(r.status_code, 503)
        self.assertIn(b'Please, check your configuration', r.content)
        self.assertFalse(Movie.objects.filter(id_kinopoisk=409424).exists())

    def test_save_view_requires_login(self):
        """SaveView should redirect unauthenticated user to login"""
        r = self.client.post(reverse('todo:save', kwargs={'id_kinopoisk': 409424}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('login', r.url)


class DetailViewTests(TestCase):

    def setUp(self):
        """Create two users and their movies with notes"""
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        self.movie1 = Movie.objects.create(
            id_kinopoisk=409424,
            type='FILM',
            title='Дюна',
            poster='https://example.com/poster.jpg'
        )
        self.movie2 = Movie.objects.create(
            id_kinopoisk=409425,
            type='FILM',
            title='Дюна 2',
            poster='https://example.com/poster2.jpg'
        )

        self.note1 = Note.objects.create(user=self.user1, movie=self.movie1)
        self.note2 = Note.objects.create(user=self.user2, movie=self.movie2)

    def test_detail_view_own_note_returns_200(self):
        """User should see their own note with status 200"""
        self.client.force_login(self.user1)
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': self.note1.id}))
        self.assertEqual(r.status_code, 200)
        self.assertIn('Дюна'.encode('utf-8'), r.content)

    def test_detail_view_others_note_returns_404(self):
        """User should not see another user's note - returns 404"""
        self.client.force_login(self.user1)
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': self.note2.id}))
        self.assertEqual(r.status_code, 404)

    def test_detail_view_unauthenticated_redirects(self):
        """Unauthenticated user should be redirected to login"""
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': self.note1.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('login', r.url)

    def test_detail_view_nonexistent_note_returns_404(self):
        """Accessing nonexistent note returns 404"""
        self.client.force_login(self.user1)
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': 99999}))
        self.assertEqual(r.status_code, 404)


class DeleteViewTests(TestCase):

    def setUp(self):
        """Create two users and their movies with notes"""
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')

        self.movie1 = Movie.objects.create(
            id_kinopoisk=409424,
            type='FILM',
            title='Дюна',
            poster='https://example.com/poster.jpg'
        )
        self.movie2 = Movie.objects.create(
            id_kinopoisk=409425,
            type='FILM',
            title='Дюна 2',
            poster='https://example.com/poster2.jpg'
        )

        self.note1 = Note.objects.create(user=self.user1, movie=self.movie1)
        self.note2 = Note.objects.create(user=self.user2, movie=self.movie2)

    def test_delete_own_note_succeeds(self):
        """User can delete their own note"""
        self.client.force_login(self.user1)
        initial_count = Note.objects.count()
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': self.note1.id}))
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Note.objects.count(), initial_count - 1)
        self.assertFalse(Note.objects.filter(id=self.note1.id).exists())

    def test_delete_others_note_returns_404(self):
        """User cannot delete another user's note - returns 404"""
        self.client.force_login(self.user1)
        initial_count = Note.objects.count()
        r = self.client.get(reverse('todo:delete', kwargs={'note_id': self.note2.id}))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(Note.objects.count(), initial_count)

    def test_delete_unauthenticated_redirects(self):
        """Unauthenticated user should be redirected to login"""
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': self.note1.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('login', r.url)
        self.assertTrue(Note.objects.filter(id=self.note1.id).exists())

    def test_delete_nonexistent_note_returns_404(self):
        """Deleting nonexistent note returns 404"""
        self.client.force_login(self.user1)
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': 99999}))
        self.assertEqual(r.status_code, 404)


class IDORTests(TestCase):
    """Tests for IDOR (Insecure Direct Object Reference) vulnerabilities"""

    def setUp(self):
        """Create two users with their own notes"""
        self.user1 = User.objects.create_user(username='alice', password='pass123')
        self.user2 = User.objects.create_user(username='bob', password='pass123')

        self.movie1 = Movie.objects.create(
            id_kinopoisk=1001,
            type='FILM',
            title='Alice Movie',
            poster='https://example.com/alice.jpg'
        )
        self.movie2 = Movie.objects.create(
            id_kinopoisk=1002,
            type='FILM',
            title='Bob Movie',
            poster='https://example.com/bob.jpg'
        )

        self.alice_note = Note.objects.create(user=self.user1, movie=self.movie1)
        self.bob_note = Note.objects.create(user=self.user2, movie=self.movie2)

    def test_idor_detail_alice_cannot_view_bob_note(self):
        """Alice should not be able to access Bob's note detail"""
        self.client.force_login(self.user1)
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': self.bob_note.id}))
        self.assertEqual(r.status_code, 404)
        self.assertNotIn(b'Bob Movie', r.content)

    def test_idor_detail_bob_cannot_view_alice_note(self):
        """Bob should not be able to access Alice's note detail"""
        self.client.force_login(self.user2)
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': self.alice_note.id}))
        self.assertEqual(r.status_code, 404)
        self.assertNotIn(b'Alice Movie', r.content)

    def test_idor_delete_alice_cannot_delete_bob_note(self):
        """Alice should not be able to delete Bob's note"""
        self.client.force_login(self.user1)
        initial_count = Note.objects.count()
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': self.bob_note.id}))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(Note.objects.count(), initial_count)
        self.assertTrue(Note.objects.filter(id=self.bob_note.id).exists())

    def test_idor_delete_bob_cannot_delete_alice_note(self):
        """Bob should not be able to delete Alice's note"""
        self.client.force_login(self.user2)
        initial_count = Note.objects.count()
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': self.alice_note.id}))
        self.assertEqual(r.status_code, 404)
        self.assertEqual(Note.objects.count(), initial_count)
        self.assertTrue(Note.objects.filter(id=self.alice_note.id).exists())


class AuthTests(TestCase):
    """Tests for authentication and authorization"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.movie = Movie.objects.create(
            id_kinopoisk=2001,
            type='FILM',
            title='Test Film',
            poster='https://example.com/test.jpg'
        )
        self.note = Note.objects.create(user=self.user, movie=self.movie)

    def test_index_view_unauthenticated_redirects(self):
        """Unauthenticated user accessing index should redirect to login"""
        r = self.client.get(reverse('todo:index'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('login', r.url)

    def test_preview_view_unauthenticated_redirects(self):
        """Unauthenticated user accessing preview should redirect to login"""
        r = self.client.get(reverse('todo:preview'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('login', r.url)

    def test_detail_view_unauthenticated_redirects(self):
        """Unauthenticated user accessing detail should redirect to login"""
        r = self.client.get(reverse('todo:detail', kwargs={'note_id': self.note.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('login', r.url)

    def test_delete_view_unauthenticated_redirects(self):
        """Unauthenticated user accessing delete should redirect to login"""
        r = self.client.post(reverse('todo:delete', kwargs={'note_id': self.note.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('login', r.url)

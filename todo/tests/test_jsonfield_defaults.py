from django.test import TestCase
from todo.models import Movie


class MovieJSONFieldDefaultsTest(TestCase):
    """Test that JSONField default=list creates independent lists for each instance."""

    def test_jsonfield_defaults_are_independent(self):
        """
        Test that modifying JSONField list in one Movie instance
        does not affect other instances.
        This verifies the fix: default=list instead of default=[].
        """
        # Create two Movie instances
        movie1 = Movie(
            id_kinopoisk=1,
            title='Movie 1',
            poster='http://example.com/1.jpg'
        )
        movie2 = Movie(
            id_kinopoisk=2,
            title='Movie 2',
            poster='http://example.com/2.jpg'
        )

        # Both should have empty lists initially
        self.assertEqual(movie1.directors, [])
        self.assertEqual(movie2.directors, [])
        self.assertIsInstance(movie1.directors, list)
        self.assertIsInstance(movie2.directors, list)

        # Modify movie1's directors list
        movie1.directors.append('Director 1')

        # movie2's directors should remain empty (independent lists)
        self.assertEqual(movie1.directors, ['Director 1'])
        self.assertEqual(movie2.directors, [])

    def test_all_jsonfield_defaults_independent(self):
        """Test that all JSONField defaults (actors, genres, countries, watchability) are independent."""
        movie1 = Movie(
            id_kinopoisk=10,
            title='Movie with cast',
            poster='http://example.com/movie1.jpg'
        )
        movie2 = Movie(
            id_kinopoisk=11,
            title='Movie without cast',
            poster='http://example.com/movie2.jpg'
        )

        # Modify multiple JSONField lists in movie1
        movie1.actors.append('Actor 1')
        movie1.genres.append('Drama')
        movie1.countries.append('USA')
        movie1.watchability.append({'url': 'https://netflix.com', 'platform': 'Netflix'})

        # movie2 should have all empty lists
        self.assertEqual(movie2.actors, [])
        self.assertEqual(movie2.genres, [])
        self.assertEqual(movie2.countries, [])
        self.assertEqual(movie2.watchability, [])

        # movie1 should have all modified lists
        self.assertEqual(len(movie1.actors), 1)
        self.assertEqual(len(movie1.genres), 1)
        self.assertEqual(len(movie1.countries), 1)
        self.assertEqual(len(movie1.watchability), 1)

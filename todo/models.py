from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    id_kinopoisk = models.IntegerField(unique=True)
    type = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=200)
    title_alternative = models.CharField(max_length=200)
    poster = models.URLField(max_length=400)
    directors = models.JSONField(default=[])
    actors = models.JSONField(default=[])
    genres = models.JSONField(default=[])
    countries = models.JSONField(default=[])
    year = models.IntegerField(null=True)
    description = models.TextField(null=True)
    slogan = models.CharField(max_length=300)
    age_rating = models.IntegerField(null=True)
    rating_kinopoisk = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    kinopoisk_votes = models.IntegerField(null=True)
    rating_imdb = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    imdb_votes = models.IntegerField(null=True)
    premiere_world = models.DateField(null=True, blank=True, verbose_name='Premiere World')
    premiere_russia = models.DateField(null=True, blank=True, verbose_name='Premiere Russia')
    watchability = models.JSONField(default=[])
    
    def __str__(self):
        return "%s - %s" % (self.id_kinopoisk, self.title)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.OneToOneField(Movie, on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')
    is_viewed = models.BooleanField(default=False)
    user_rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "%s - %s" % (self.user, self.movie.title)

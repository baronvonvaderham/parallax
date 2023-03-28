from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import MOVIE_RATINGS
from core.models import BaseModel
from library.models import MovieLibrary
from media.models import Genre, Credit, Tag


class MovieManager(models.Manager):
    pass


class Movie(BaseModel):
    title = models.CharField(_('title'), max_length=256, null=False)
    sort_title = models.CharField(_('sort title'), max_length=256, null=False)
    alternate_title = models.CharField(_('alternate title'), max_length=256, blank=True, null=True)
    release_date = models.DateField(_('release date'), blank=True, null=True)
    studio = models.CharField(_('studio'), max_length=128, blank=True, null=True)
    movie_rating = models.CharField(_('movie rating'), max_length=8, choices=MOVIE_RATINGS)
    tagline = models.TextField(_('tagline'), blank=True, null=True)
    summary = models.TextField(_('summary'), blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)
    country = models.CharField(_('country'), max_length=8, blank=True, null=True)

    # Library relationship can be null so the movie can be re-claimed by a new library,
    # saving having to retrieve metadata again.
    library = models.ForeignKey(MovieLibrary, null=True, on_delete=models.SET_NULL)
    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Credit)
    tags = models.ManyToManyField(Tag)

    objects = MovieManager()

    class Meta:
        verbose_name = _('movie')
        verbose_name_plural = _('movies')

import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import MOVIE_RATINGS
from core.models import BaseModel
from library.models import MovieLibrary
from media.exceptions import InvalidFilepathError
from media.constants import VALID_VIDEO_EXTENSIONS
from media.models import Genre, Credit, Tag
from media.utils import generate_sort_title
from metadata.tmdb.service import TheMovieDatabaseService


class MovieManager(models.Manager):

    def create_from_file(self, filepath):
        if not self._validate_filepath(filepath=filepath):
            raise InvalidFilepathError(filepath)
        title, year = self._get_title_year_from_filepath(filepath)
        kwargs = {
            'query': title,
            'year': year,
        }
        service = TheMovieDatabaseService()
        id = service.retrieve_id(kind='movie', **kwargs)
        kwargs = service.retrieve_metadata(kind='movie', id=id)
        genres = kwargs.pop('genres')
        credits = kwargs.pop('credits')
        movie = self.create(**kwargs)
        genre_objects = [Genre.objects.get_or_create(**genre)[0] for genre in genres]
        credit_objects = [Credit.objects.get_or_create(**credit)[0] for credit in credits]
        movie.genres.add(*genre_objects)
        movie.credits.add(*credit_objects)
        return movie

    @staticmethod
    def _validate_filepath(filepath):
        return os.path.splitext(filepath)[-1] in VALID_VIDEO_EXTENSIONS

    @staticmethod
    def _get_title_year_from_filepath(filepath):
        parts = os.path.splitext(filepath)[0].split('/')
        title, year = parts[-1].split('(')
        return ' '.join(title.split(' ')[:-1]), year.replace(')', '')


class Movie(BaseModel):
    title = models.CharField(_('title'), max_length=256, null=False)
    sort_title = models.CharField(_('sort title'), max_length=256, null=False)
    alternate_title = models.CharField(_('alternate title'), max_length=256, blank=True, null=True)
    release_date = models.DateField(_('release date'), blank=True, null=True)
    studio = models.CharField(_('studio'), max_length=128, blank=True, null=True)
    movie_rating = models.CharField(_('movie rating'), max_length=8, choices=MOVIE_RATINGS, blank=True, null=True)
    tagline = models.TextField(_('tagline'), blank=True, null=True)
    summary = models.TextField(_('summary'), blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)
    country = models.CharField(_('country'), max_length=56, blank=True, null=True)

    # Library relationship can be null so the movie can be re-claimed by a new library,
    # saving having to retrieve metadata again.
    library = models.ForeignKey(MovieLibrary, blank=True, null=True, on_delete=models.SET_NULL)
    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Credit)
    tags = models.ManyToManyField(Tag)

    objects = MovieManager()

    class Meta:
        verbose_name = _('movie')
        verbose_name_plural = _('tmdb')

    def __init__(self, **kwargs):
        super().__init__()
        self.title = kwargs.get('title')
        self.sort_title = kwargs.get('sort_title') if kwargs.get('sort_title') else generate_sort_title(self.title)
        self.alternate_title = kwargs.get('alternate_title')
        self.release_date = kwargs.get('release_date')
        self.studio = kwargs.get('studio')
        self.movie_rating = kwargs.get('movie_rating')
        self.tagline = kwargs.get('tagline')
        self.summary = kwargs.get('summary')
        self.poster_image = kwargs.get('poster_image')
        self.country = kwargs.get('country')

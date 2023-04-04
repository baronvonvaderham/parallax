import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from media.exceptions import InvalidFilepathError, DuplicateMediaError
from server.models import Server


logger = logging.getLogger(__name__)


class Library(BaseModel):
    name = models.CharField(_('name'), max_length=128, null=False, default="MyLibrary")
    folder = models.CharField(_('folder'), max_length=1024, blank=False, null=True)
    cover_photo = models.CharField(_('cover photo'), max_length=128, blank=True, null=True)
    server = models.ForeignKey(Server, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        abstract = True

    def __init__(self, **kwargs):
        super().__init__()
        self.name = kwargs.get('name')
        self.folder = kwargs.get('folder')
        self.cover_photo = kwargs.get('cover_photo')
        self.server = kwargs.get('server')

    def __str__(self):
        return self.name


class MovieLibraryManager(models.Manager):
    pass


class MovieLibrary(Library):
    objects = MovieLibraryManager()

    def add_movie_from_file(self, filepath):
        from media.movies.models import Movie
        try:
            movie = Movie.objects.create_from_file(filepath)
            return self.add_existing_movie(movie=movie)
        except InvalidFilepathError as e:
            logger.error(f'Unable to add movie to library: {e}')
        except DuplicateMediaError as e:
            logger.warning(f'Movie already exists, adding existing movie to library.')
            movie = Movie.objects.get(filepath=filepath)
            return self.add_existing_movie(movie=movie)

    def add_existing_movie(self, movie):
        try:
            self.movies.add(movie)
            return True
        except Exception as e:
            logger.exception(f'Exception while attempting to add movie {movie} to library {self}: {e}')


class ShowLibraryManager(models.Manager):
    pass


class ShowLibrary(Library):
    objects = ShowLibraryManager()


class VideoLibraryManager(models.Manager):
    pass


class VideoLibrary(Library):
    objects = VideoLibraryManager()

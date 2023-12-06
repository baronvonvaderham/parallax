import logging
import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, User
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
    authorized_users = models.ManyToManyField(User, blank=True, related_name='movie_libraries', symmetrical=False)

    objects = MovieLibraryManager()

    def add_movie_from_file(self, filepath):
        """
        Adds a new movie to the library at the given filepath.
        (if the movie already exists in the database, the existing movie is added)
        """
        from media.movies.models import Movie
        try:
            movie = Movie.objects.create_from_file(filepath)
            return self.add_existing_movie(movie=movie)
        except InvalidFilepathError as e:
            logger.error(f'Unable to add movie to library: {e}')
        except DuplicateMediaError as e:
            # If a duplicate is found, simple add that existing movie instead
            logger.warning(f'Movie already exists, adding existing movie to library.')
            movie = Movie.objects.get(filepath=filepath)
            return self.add_existing_movie(movie=movie)

    def add_existing_movie(self, movie):
        try:
            self.movies.add(movie)
            return True
        except Exception as e:
            logger.exception(f'Exception while attempting to add movie {movie} to library {self}: {e}')
            return False


class ShowLibraryManager(models.Manager):
    pass


class ShowLibrary(Library):
    authorized_users = models.ManyToManyField(User, blank=True, related_name='show_libraries', symmetrical=False)

    objects = ShowLibraryManager()

    def add_new_show_from_directory(self, filepath):
        """
        Adds a new show to the library at the given filepath. Also adds the seasons (from subfolders)
        and then adds the episodes for each of those seasons (from filenames).
        """
        from media.shows.models import Show, Season, Episode

        # Step 1) Create the Show with its metadata.
        try:
            show = Show.objects.create_from_directory(filepath=filepath)
            self.shows.add(show)
        except DuplicateMediaError as e:
            # If a duplicate is found, simple add that existing movie instead
            logger.warning(f'Movie already exists, adding existing movie to library.')
            show = Show.objects.get(filepath=filepath)
            return self.add_existing_show(show=show)

        try:
            # Step 2) Create the seasons for the show and attach them.
            seasons = [x[0] for x in os.walk(filepath)]
            seasons.reverse()  # For some reason this always ends up in reverse numerical order and that bugs me
            for season_path in seasons:
                subdir_name = season_path.split('/')[-1].lower()
                if not subdir_name.startswith('season') or subdir_name.startswith('series'):
                    continue
                season_num = int(subdir_name.split(' ')[-1])
                season = Season.objects.create_season(show=show, season_number=season_num)
                # Step 3) Create the episodes for each season.
                episodes = os.listdir(season_path)
                episodes.reverse()
                for file in episodes:
                    episode_filepath = f'{season_path}/{file}'
                    episode_num = file.split(' ')[0]
                    Episode.objects.create_episode(episode_number=episode_num, season=season, filepath=episode_filepath)
            return True
        except (DuplicateMediaError, InvalidFilepathError) as e:
            logger.error(f'Error occurred while importing show: {e}')
            return False

    def add_existing_show(self, show):
        try:
            self.shows.add(show)
            return True
        except Exception as e:
            logger.exception(f'Exception while attempting to add show {show} to library {self}: {e}')
            return False


class VideoLibraryManager(models.Manager):
    pass


class VideoLibrary(Library):
    authorized_users = models.ManyToManyField(User, blank=True, related_name='video_libraries', symmetrical=False)

    objects = VideoLibraryManager()

    def add_video_from_file(self, filepath):
        """
        Adds a new video to the library from the given filepath.

        TODO: Add automatic import of metadata from the file's EXIF data.
        """
        from media.videos.models import Video

        try:
            video = Video.objects.create_video(filepath=filepath)
            return self.add_existing_video(video)
        except InvalidFilepathError as e:
            logger.error(f'Unable to add video to library: {e}')
        except DuplicateMediaError as e:
            # If a duplicate is found, simple add that existing movie instead
            logger.warning(f'Movie already exists, adding existing movie to library.')
            video = Video.objects.get(filepath=filepath)
            return self.add_existing_video(video=video)

    def add_existing_video(self, video):
        try:
            self.videos.add(video)
            return True
        except Exception as e:
            logger.exception(f'Exception while attempting to add video {video} to library {self}: {e}')
            return False

import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from library.models import ShowLibrary
from media.exceptions import DuplicateMediaError
from media.models import Genre, Credit, Tag
from media.shows.constants import TV_AUDIENCE_LABEL, TV_CONTENT_LABEL
from media.utils import generate_sort_title, get_title_year_from_filepath
from metadata.tmdb.service import TheMovieDatabaseService


class ShowManager(models.Manager):

    def create_from_directory(self, filepath):
        if self._check_if_show_exists(filepath):
            raise DuplicateMediaError(filepath=filepath, media_type='Show')
        title, year = get_title_year_from_filepath(filepath=filepath)
        kwargs = {'query': title}
        service = TheMovieDatabaseService()
        id = service.retrieve_id(kind='tv', **kwargs)
        kwargs = service.retrieve_metadata(kind='tv', id=id)
        kwargs['filepath'] = filepath
        kwargs['tmdb_id'] = id
        genres = kwargs.pop('genres')
        show = self.create(**kwargs)
        genre_objects = [Genre.objects.get_or_create(**genre)[0] for genre in genres]
        show.genres.add(*genre_objects)
        return show

    @staticmethod
    def _check_if_show_exists(filepath):
        show = Show.objects.filter(filepath=filepath).first()
        if isinstance(show, Show):
            return True
        return False


class Show(BaseModel):
    filepath = models.CharField(_('filepath'), max_length=1024, blank=True, null=True)
    title = models.CharField(_('title'), max_length=256, null=False)
    sort_title = models.CharField(_('sort title'), max_length=256, null=False)
    alternate_title = models.CharField(_('alternate title'), max_length=256, blank=True, null=True)
    premiere_date = models.DateField(_('premiere date'), blank=True, null=True)
    network = models.CharField(_('network'), max_length=56, blank=True, null=True)
    summary = models.TextField(_('summary'), blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)
    country = models.CharField(_('country'), max_length=8, blank=True, null=True)
    tmdb_id = models.IntegerField(_('tmdb_id'), blank=True, null=True)

    # Library relationship can be null so the movie can be re-claimed by a new library,
    # saving having to retrieve metadata again.
    library = models.ForeignKey(ShowLibrary, blank=True, null=True, on_delete=models.SET_NULL, related_name='shows')
    genres = models.ManyToManyField(Genre)
    tags = models.ManyToManyField(Tag)

    objects = ShowManager()

    class Meta:
        verbose_name = _('show')
        verbose_name_plural = _('shows')

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if kwargs:
            self.filepath = kwargs.get('filepath')
            self.title = kwargs.get('title')
            self.sort_title = kwargs.get('sort_title') if kwargs.get('sort_title') else generate_sort_title(self.title)
            self.alternate_title = kwargs.get('alternate_title')
            self.premiere_date = kwargs.get('premiere_date')
            self.network = kwargs.get('network')
            self.summary = kwargs.get('summary')
            self.poster_image = kwargs.get('poster_image')
            self.country = kwargs.get('country')
            self.tmdb_id = kwargs.get('tmdb_id')
            if kwargs.get('library'):
                self.library = kwargs.get('library')
            if kwargs.get('genres'):
                self.genres = kwargs.get('genres')
            if kwargs.get('tags'):
                self.tags = kwargs.get('tags')

    def __str__(self):
        return self.title


class SeasonManager(models.Manager):

    def create_season(self, season_number, show):
        if self._check_if_season_exists(show=show, season_num=season_number):
            raise DuplicateMediaError(media_type='Season', show=show)
        service = TheMovieDatabaseService()
        kwargs = service.retrieve_metadata(kind='tv', id=show.tmdb_id, season_num=season_number)
        kwargs['show'] = show
        season = self.create(**kwargs)
        return season

    @staticmethod
    def _check_if_season_exists(show, season_num):
        return season_num in [season.number for season in show.seasons.all()]


class Season(BaseModel):
    number = models.IntegerField(_('number'), blank=True, null=True)
    start_date = models.DateField(_('start date'), blank=True, null=True)
    summary = models.TextField(_('summary'), blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)

    show = models.ForeignKey(Show, null=False, on_delete=models.CASCADE, related_name='seasons')

    objects = SeasonManager()

    class Meta:
        verbose_name = _('season')
        verbose_name_plural = _('seasons')

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if kwargs:
            self.number = kwargs.get('number')
            self.start_date = kwargs.get('start_date')
            self.end_date = kwargs.get('end_date')
            self.poster_image = kwargs.get('poster_image')
            self.show = kwargs.get('show')

    def __str__(self):
        return f'{self.show.title} - Season {self.number}'


class EpisodeManager(models.Manager):

    def create_episode(self, episode_number, season):
        if self._check_if_episode_exists(season=season, episode_num=episode_number):
            raise DuplicateMediaError(media_type='Episode', show=season.show)
        service = TheMovieDatabaseService()
        kwargs = service.retrieve_metadata(kind='tv', id=season.show.tmdb_id, season_num=season.number,
                                           episode_num=episode_number)
        kwargs['season'] = season
        episode = self.create(**kwargs)
        return episode

    @staticmethod
    def _check_if_episode_exists(season, episode_num):
        return episode_num in [episode.number for episode in season.episodes.all()]


class Episode(BaseModel):
    filepath = models.CharField(_('filepath'), max_length=1024, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    title = models.CharField(_('title'), max_length=256, blank=True, null=True)
    air_date = models.DateField(_('air date'), blank=True, null=True)
    tv_audience_label = models.CharField(choices=TV_AUDIENCE_LABEL, max_length=8, blank=True, null=True)
    tv_content_label = models.CharField(choices=TV_CONTENT_LABEL, max_length=8, blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)

    credits = models.ManyToManyField(Credit)
    season = models.ForeignKey(Season, null=False, on_delete=models.CASCADE, related_name='episodes')

    objects = EpisodeManager()

    class Meta:
        verbose_name = _('episode')
        verbose_name_plural = _('episodes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if kwargs:
            self.filepath = kwargs.get('filepath')
            self.number = kwargs.get('number')
            self.title = kwargs.get('title')
            self.air_date = kwargs.get('air_date')
            self.tv_audience_label = kwargs.get('tv_audience_label')
            self.tv_content_label = kwargs.get('tv_content_label')
            self.poster_image = kwargs.get('poster_image')
            self.season = kwargs.get('season')

    def __str__(self):
        return self.title

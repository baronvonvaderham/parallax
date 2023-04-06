import datetime
import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from library.models import VideoLibrary
from media.exceptions import DuplicateMediaError, InvalidFilepathError
from media.models import Genre, Credit, Tag
from media.utils import generate_sort_title, validate_filepath, get_title_year_from_filepath


class VideoManager(models.Manager):

    def create_video(self, filepath):
        if not validate_filepath(filepath=filepath):
            raise InvalidFilepathError(filepath)
        if self._check_if_video_exists(filepath=filepath):
            raise DuplicateMediaError(media_type='Video', filepath=filepath)
        kwargs = self._construct_video_data(filepath=filepath)
        video = self.create(**kwargs)
        return video

    @staticmethod
    def _check_if_video_exists(filepath):
        video = Video.objects.filter(filepath=filepath).first()
        if isinstance(video, Video):
            return True
        return False

    @staticmethod
    def _construct_video_data(filepath):
        title, year = get_title_year_from_filepath(filepath=filepath)
        data = {'title': title}
        if year:
            data['release_date']: datetime.date(year=year, month=1, day=1)
        return data


class Video(BaseModel):
    filepath = models.CharField(_('filepath'), max_length=1024, blank=True, null=True)
    title = models.CharField(_('title'), max_length=256, null=False)
    sort_title = models.CharField(_('title'), max_length=256, null=False)
    release_date = models.DateField(_('release date'), blank=True, null=True)
    summary = models.TextField('summary', blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)
    country = models.CharField(_('country'), max_length=8, blank=True, null=True)

    library = models.ForeignKey(VideoLibrary, blank=True, null=True, on_delete=models.PROTECT, related_name='videos')
    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Credit)
    tags = models.ManyToManyField(Tag)

    objects = VideoManager()

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if kwargs:
            self.filepath = kwargs.get('filepath')
            self.title = kwargs.get('title')
            self.sort_title = kwargs.get('sort_title') if kwargs.get('sort_title') else generate_sort_title(self.title)
            self.release_date = kwargs.get('release_date')
            self.summary = kwargs.get('summary')
            self.poster_image = kwargs.get('poster_image')
            self.country = kwargs.get('country')
            self.library = kwargs.get('library')

    def __str__(self):
        return f'{self.title} ({self.release_date.year}'

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from media.models import Genre, Credit, Tag


class VideoManager(models.Manager):
    pass


class Video(BaseModel):
    title = models.CharField(_('title'), max_length=256, null=False)
    sort_title = models.CharField(_('title'), max_length=256, null=False)
    air_date = models.DateField(_('air date'), blank=True, null=True)
    summary = models.TextField('summary', blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)
    country = models.CharField(_('country'), max_length=8, blank=True, null=True)

    genres = models.ManyToManyField(Genre)
    credits = models.ManyToManyField(Credit)
    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')

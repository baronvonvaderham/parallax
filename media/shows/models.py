from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import TV_AUDIENCE_LABEL, TV_CONTENT_LABEL
from media.models import Genre, Credit, Tag
from core.models import BaseModel


class ShowManager(models.Manager):
    pass


class Show(BaseModel):
    title = models.CharField(_('title'), max_length=256, null=False)
    sort_title = models.CharField(_('sort title'), max_length=256, null=False)
    alternate_title = models.CharField(_('alternate title'), max_length=256, blank=True, null=True)
    premiere_date = models.DateField(_('premiere date'), blank=True, null=True)
    network = models.CharField(_('network'), max_length=56, blank=True, null=True)
    summary = models.TextField(_('summary'), blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)
    country = models.CharField(_('country'), max_length=8, blank=True, null=True)

    genres = models.ManyToManyField(Genre)
    tags = models.ManyToManyField(Tag)

    objects = ShowManager()

    class Meta:
        verbose_name = _('show')
        verbose_name_plural = _('shows')


class SeasonManager(models.Manager):
    pass


class Season(BaseModel):
    number = models.IntegerField(_('number'), null=False)
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('start date'), blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)

    show = models.ForeignKey(Show, null=False, on_delete=models.CASCADE)

    objects = SeasonManager()

    class Meta:
        verbose_name = _('season')
        verbose_name_plural = _('seasons')


class EpisodeManager(models.Manager):
    pass


class Episode(BaseModel):
    number = models.IntegerField(null=False)
    title = models.CharField(_('title'), max_length=256, blank=True, null=True)
    air_date = models.DateField(_('air date'), blank=True, null=True)
    tv_audience_label = models.CharField(choices=TV_AUDIENCE_LABEL, max_length=8, blank=True, null=True)
    tv_content_label = models.CharField(choices=TV_CONTENT_LABEL, max_length=8, blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)

    credits = models.ManyToManyField(Credit)

    objects = EpisodeManager()

    class Meta:
        verbose_name = _('episode')
        verbose_name_plural = _('episodes')

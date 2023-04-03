from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from library.models import ShowLibrary
from media.models import Genre, Credit, Tag
from media.shows.constants import TV_AUDIENCE_LABEL, TV_CONTENT_LABEL
from media.utils import generate_sort_title


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

    # Library relationship can be null so the movie can be re-claimed by a new library,
    # saving having to retrieve metadata again.
    library = models.ForeignKey(ShowLibrary, blank=True, null=True, on_delete=models.SET_NULL)
    genres = models.ManyToManyField(Genre)
    tags = models.ManyToManyField(Tag)

    objects = ShowManager()

    class Meta:
        verbose_name = _('show')
        verbose_name_plural = _('shows')

    def __init__(self, **kwargs):
        super().__init__()
        self.title = kwargs.get('title')
        self.sort_title = kwargs.get('sort_title') if kwargs.get('sort_title') else generate_sort_title(self.title)
        self.alternate_title = kwargs.get('alternate_title')
        self.premiere_date = kwargs.get('premiere_date')
        self.network = kwargs.get('network')
        self.summary = kwargs.get('summary')
        self.poster_image = kwargs.get('poster_image')
        self.country = kwargs.get('country')
        if kwargs.get('library'):
            self.library = kwargs.get('library')
        if kwargs.get('genres'):
            self.genres = kwargs.get('genres')
        if kwargs.get('tags'):
            self.tags = kwargs.get('tags')

    def __str__(self):
        return f'{self.title} ({self.premiere_date.year})'


class SeasonManager(models.Manager):
    pass


class Season(BaseModel):
    number = models.IntegerField(_('number'), blank=True, null=True)
    start_date = models.DateField(_('start date'), blank=True, null=True)
    end_date = models.DateField(_('start date'), blank=True, null=True)
    poster_image = models.CharField(_('poster image'), max_length=128, blank=True, null=True)

    show = models.ForeignKey(Show, null=False, on_delete=models.CASCADE)

    objects = SeasonManager()

    class Meta:
        verbose_name = _('season')
        verbose_name_plural = _('seasons')

    def __init__(self, **kwargs):
        super().__init__()
        self.number = kwargs.get('number')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')
        self.poster_image = kwargs.get('poster_image')
        self.show = kwargs.get('show')

    def __str__(self):
        return f'{self.show.name} - Season {self.number}'


class EpisodeManager(models.Manager):
    pass


class Episode(BaseModel):
    filepath = models.CharField(_('filepath'), max_length=1024, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
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

    def __init__(self, **kwargs):
        super().__init__()
        self.filepath = kwargs.get('filepath')
        self.number = kwargs.get('number')
        self.title = kwargs.get('title')
        self.air_date = kwargs.get('air_date')
        self.tv_audience_label = kwargs.get('tv_audience_label')
        self.tv_content_label = kwargs.get('tv_content_label')
        self.poster_image = kwargs.get('poster_image')

    def __str__(self):
        return self.title

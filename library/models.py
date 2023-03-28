from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from server.models import Server


class Library(BaseModel):
    name = models.CharField(_('name'), max_length=128, null=False, default="MyLibrary")
    cover_photo = models.CharField(_('cover photo'), max_length=128, blank=True, null=True)
    server = models.ForeignKey(Server, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        abstract = True

    def __init__(self, **kwargs):
        super().__init__()
        self.name = kwargs.get('name')
        self.cover_photo = kwargs.get('cover_photo')
        self.server = kwargs.get('server')


class MovieLibraryManager(models.Manager):
    pass


class MovieLibrary(Library):
    objects = MovieLibraryManager()


class ShowLibraryManager(models.Manager):
    pass


class ShowLibrary(Library):
    objects = ShowLibraryManager()


class VideoLibraryManager(models.Manager):
    pass


class VideoLibrary(Library):
    objects = VideoLibraryManager()

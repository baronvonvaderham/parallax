from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from server.models import Server


class Library(object):
    name = models.CharField(_('name'), max_length=128, null=False)
    cover_photo = models.CharField(_('cover photo'), max_length=128, blank=True, null=True)
    server = models.ForeignKey(Server, null=False, on_delete=models.PROTECT)


class MovieLibraryManager(models.Manager):
    pass


class MovieLibrary(Library, BaseModel):
    objects = MovieLibraryManager()


class ShowLibraryManager(models.Manager):
    pass


class ShowLibrary(Library, BaseModel):
    objects = ShowLibraryManager()


class VideoLibraryManager(models.Manager):
    pass


class VideoLibrary(Library, BaseModel):
    objects = VideoLibraryManager()

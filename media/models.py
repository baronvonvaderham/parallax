from django.db import models
from django.utils.translation import gettext_lazy as _


from core.models import BaseModel


class Genre(BaseModel):
    name = models.CharField(_('name'), max_length=32, null=False)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Credit(BaseModel):
    name = models.CharField(_('name'), max_length=128, null=False)
    role = models.CharField(_('role'), max_length=128, null=False)

    class Meta:
        unique_together = [['name', 'role']]


class Tag(BaseModel):
    name = models.CharField(_('name'), max_length=128, null=False, unique=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

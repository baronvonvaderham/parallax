from django.db import models
from django.utils.translation import gettext_lazy as _


from core.models import BaseModel
from media.constants import CREDIT_TYPES


class Genre(BaseModel):
    name = models.CharField(_('name'), max_length=32, null=False)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Credit(BaseModel):
    name = models.CharField(_('name'), max_length=128, null=False)
    role = models.CharField(_('role'), max_length=128, null=False)
    type = models.CharField(_('type'), choices=CREDIT_TYPES, max_length=4, null=False)

    class Meta:
        unique_together = [['name', 'role']]

    def __str__(self):
        return f'{self.name} -- {self.role}'


class Tag(BaseModel):
    name = models.CharField(_('name'), max_length=128, null=False, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name

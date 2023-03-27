import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Base class for all DB models to inherit from for consistency
    of applying fields and methods common to all DB tables.
    """

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class UserManager(models.Manager):
    pass


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=28, unique=True)

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

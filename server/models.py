from django.db import models
from django.utils.translation import gettext_lazy as _

from languages_plus.models import Language
from core.models import BaseModel, User
from .constants import SERVER_DEFAULTS


class ServerManager(models.Manager):
    pass


class Server(BaseModel):
    name = models.CharField(_('name'), max_length=32, blank=False, null=False)
    remote_access = models.BooleanField(_('remote access'), default=True)
    public_port = models.IntegerField(_('public port'), default=SERVER_DEFAULTS.get('PUBLIC_PORT'))
    upload_limit = models.IntegerField(_('upload limit'), default=SERVER_DEFAULTS.get('UPLOAD_LIMIT'))
    scan_automatically = models.BooleanField(_('scan automatically'), default=True)
    changes_detected_scan = models.BooleanField(_('changes detected scan'), default=True)
    scheduled_scan_enabled = models.BooleanField(_('scheduled scan enabled'), default=False)
    scheduled_scan_interval = models.IntegerField(
        _('scheduled scan interval'),
        default=SERVER_DEFAULTS.get('SCHEDULED_SCAN_INTERVAL')
    )
    empty_trash_after_scan = models.BooleanField(_('empty trash after scan'), default=True)
    allow_delete = models.BooleanField(_('allow delete'), default=True)
    queue_retention_interval = models.IntegerField(
        _('queue retention interval'),
        default=SERVER_DEFAULTS.get('QUEUE_RETENTION_INTERVAL')
    )
    max_queue_size = models.IntegerField(_('max queue size'), default=SERVER_DEFAULTS.get('MAX_QUEUE_SIZE'))
    played_threshold = models.IntegerField(_('played threshold'), default=SERVER_DEFAULTS.get('PLAYED_THRESHOLD'))
    paused_termination_limit = models.IntegerField(
        _('paused termination limit'),
        default=SERVER_DEFAULTS.get('PAUSED_TERMINATION_LIMIT')
    )
    max_stream_count = models.IntegerField(_('max stream count'), default=SERVER_DEFAULTS.get('MAX_STREAM_COUNT'))
    transcoding_enabled = models.BooleanField(_('transcoding enabled'), default=True)
    max_transcode_count = models.IntegerField(
        _('max transcode count'),
        default=SERVER_DEFAULTS.get('MAX_TRANSCODE_COUNT')
    )

    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name=_('owner'))
    authorized_users = models.ManyToManyField(User, related_name=_('authorized_users'))
    preferred_language = models.ForeignKey(Language, on_delete=models.PROTECT, blank=True, null=True)

    objects = ServerManager()

    class Meta:
        verbose_name = _('server')
        verbose_name_plural = _('servers')
        # Owner cannot have multiple servers with the same name
        unique_together = [['name', 'owner']]

    @property
    def language(self):
        return self.preferred_language.name_en

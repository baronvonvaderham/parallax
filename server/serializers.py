from languages_plus.models import Language
from rest_framework import serializers

from core.serializers import UserSerializer
from server.constants import SERVER_DEFAULTS
from server.models import Server


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = []


class ServerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=32)
    remote_access = serializers.BooleanField(required=False, default=True)
    public_port = serializers.IntegerField(required=False, default=SERVER_DEFAULTS.get('PUBLIC_PORT'))
    upload_limit = serializers.IntegerField(required=False, default=SERVER_DEFAULTS.get('UPLOAD_LIMIT'))
    scan_automatically = serializers.BooleanField(required=False, default=True)
    changes_detected_scan = serializers.BooleanField(required=False, default=True)
    scheduled_scan_enabled = serializers.BooleanField(required=False, default=False)
    scheduled_scan_interval = serializers.IntegerField(
        required=False, default=SERVER_DEFAULTS.get('SCHEDULED_SCAN_INTERVAL'))
    empty_trash_after_scan = serializers.BooleanField(required=False, default=True)
    allow_delete = serializers.BooleanField(required=False, default=True)
    queue_retention_interval = serializers.IntegerField(
        required=False, default=SERVER_DEFAULTS.get('QUEUE_RETENTION_INTERVAL'))
    max_queue_size = serializers.IntegerField(required=False, default=SERVER_DEFAULTS.get('MAX_QUEUE_SIZE'))
    played_threshold = serializers.IntegerField(required=False, default=SERVER_DEFAULTS.get('PLAYED_THRESHOLD'))
    paused_termination_limit = serializers.IntegerField(
        required=False, default=SERVER_DEFAULTS.get('PAUSED_TERMINATION_LIMIT'))
    max_stream_count = serializers.IntegerField(required=False, default=SERVER_DEFAULTS.get('MAX_STREAM_COUNT'))
    transcoding_enabled = serializers.BooleanField(required=False, default=True)
    max_transcode_count = serializers.IntegerField(required=False, default=SERVER_DEFAULTS.get('MAX_TRANSCODE_COUNT'))

    owner = UserSerializer()
    authorized_users = UserSerializer(many=True)
    preferred_language = LanguageSerializer()

    class Meta:
        model = Server
        fields = ['name', 'remote_access', 'public_port', 'upload_limit', 'scan_automatically', 'changes_detected_scan',
                  'scheduled_scan_enabled', 'scheduled_scan_interval', 'empty_trash_after_scan', 'allow_delete',
                  'queue_retention_interval', 'max_queue_size', 'played_threshold', 'paused_termination_limit',
                  'max_stream_count', 'transcoding_enabled', 'max_transcode_count', 'owner', 'authorized_users',
                  'preferred_language']

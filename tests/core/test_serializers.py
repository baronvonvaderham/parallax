import pytest

from core.serializers import UserSerializer
from server.constants import SERVER_DEFAULTS
from server.serializers import ServerSerializer


def test_user_serializer(user):
    serializer = UserSerializer(instance=user)
    assert serializer.data['email'] == 'feynman@caltech.edu'
    assert serializer.data['username'] == 'Feynman'


def test_server_serializer(server, user):
    serializer = ServerSerializer(instance=server)
    assert serializer.data['name'] == 'MyServer'
    assert serializer.data['remote_access']
    assert serializer.data['public_port'] == SERVER_DEFAULTS.get('PUBLIC_PORT')
    assert serializer.data['upload_limit'] == SERVER_DEFAULTS.get('UPLOAD_LIMIT')
    assert serializer.data['scan_automatically']
    assert serializer.data['changes_detected_scan']
    assert not serializer.data['scheduled_scan_enabled']
    assert serializer.data['scheduled_scan_interval'] == SERVER_DEFAULTS.get('SCHEDULED_SCAN_INTERVAL')
    assert serializer.data['empty_trash_after_scan']
    assert serializer.data['allow_delete']
    assert serializer.data['queue_retention_interval'] == SERVER_DEFAULTS.get('QUEUE_RETENTION_INTERVAL')
    assert serializer.data['max_queue_size'] == SERVER_DEFAULTS.get('MAX_QUEUE_SIZE')
    assert serializer.data['played_threshold'] == SERVER_DEFAULTS.get('PLAYED_THRESHOLD')
    assert serializer.data['paused_termination_limit'] == SERVER_DEFAULTS.get('PAUSED_TERMINATION_LIMIT')
    assert serializer.data['max_stream_count'] == SERVER_DEFAULTS.get('MAX_STREAM_COUNT')
    assert serializer.data['transcoding_enabled']
    assert serializer.data['max_transcode_count'] == SERVER_DEFAULTS.get('MAX_TRANSCODE_COUNT')
    assert serializer.data['owner'] == UserSerializer(instance=user).data
    assert not serializer.data['authorized_users']
    assert not serializer.data['preferred_language']

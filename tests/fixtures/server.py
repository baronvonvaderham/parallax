import pytest

from server.models import Server


@pytest.fixture
def create_server():
    """
    A function to create 'server.Server' instances
    """
    from server.models import Server

    def _create_server(**kwargs):
        return Server.objects.create(**kwargs)

    return _create_server


@pytest.fixture
def server(create_server, user):
    """
    A default server.Server instance.
    """
    kwargs = {
        'name': 'MyServer',
        'owner': user,
    }
    return create_server(**kwargs)

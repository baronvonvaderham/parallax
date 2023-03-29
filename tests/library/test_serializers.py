import pytest

from library.serializers import (
    MovieLibrarySerializer,
    ShowLibrarySerializer,
    VideoLibrarySerializer,
)


def test_movie_library_serializer(movie_library, server, user):
    serializer = MovieLibrarySerializer(instance=movie_library)
    assert serializer.data['name'] == movie_library.name
    assert not serializer.data['cover_photo']
    assert serializer.data['server'].get('name') == 'MyServer'


def test_show_library_serializer(show_library, server, user):
    serializer = ShowLibrarySerializer(instance=show_library)
    assert serializer.data['name'] == show_library.name
    assert not serializer.data['cover_photo']
    assert serializer.data['server'].get('name') == 'MyServer'


def test_video_library_serializer(video_library, server, user):
    serializer = VideoLibrarySerializer(instance=video_library)
    assert serializer.data['name'] == video_library.name
    assert not serializer.data['cover_photo']
    assert serializer.data['server'].get('name') == 'MyServer'



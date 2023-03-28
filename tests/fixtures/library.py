import pytest


@pytest.fixture
def create_movie_library():
    """
    A function to create 'library.MovieLibrary' instances
    """
    from library.models import MovieLibrary

    def _create_movie_library(**kwargs):
        return MovieLibrary.objects.create(**kwargs)

    return _create_movie_library


@pytest.fixture
def movie_library(create_movie_library, server):
    """
    A default 'library.MovieLibrary' instance.
    """
    return create_movie_library(name='MyMovies', server=server)


@pytest.fixture
def create_show_library():
    """
    A function to create 'library.ShowLibrary' instances
    """
    from library.models import ShowLibrary

    def _create_show_library(**kwargs):
        return ShowLibrary.objects.create(**kwargs)

    return _create_show_library


@pytest.fixture
def show_library(create_show_library, server):
    """
    A default 'library.ShowLibrary' instance.
    """
    return create_show_library(name='MyShows', server=server)


@pytest.fixture
def create_video_library():
    """
    A function to create 'library.VideoLibrary' instances
    """
    from library.models import VideoLibrary

    def _create_video_library(**kwargs):
        return VideoLibrary.objects.create(**kwargs)

    return _create_video_library


@pytest.fixture
def video_library(create_video_library, server):
    """
    A default 'library.VideoLibrary' instance.
    """
    return create_video_library(name='MyVideos', server=server)

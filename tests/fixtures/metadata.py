import pytest


@pytest.fixture
def tmdb_service():
    """
    The Movie Database Service class instance.
    """
    from metadata.tmdb.service import TheMovieDatabaseService

    return TheMovieDatabaseService()

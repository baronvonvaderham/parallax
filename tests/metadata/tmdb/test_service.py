import pytest

from metadata.tmdb.service import TheMovieDatabaseService
from parallax import settings


class TestTMDBService:

    def test_init_service(self, tmdb_service):

        assert isinstance(tmdb_service, TheMovieDatabaseService)
        assert tmdb_service.api_key == settings.TMDB_V3_API_KEY

    def test_get_path(self, tmdb_service):
        method = 'search'
        kind = 'movie'
        path = tmdb_service._get_path(method=method, kind=kind)
        assert path == 'https://api.themoviedb.org/3/search/movie'

    def test_search__movie_title(self, tmdb_service):
        kwargs = {
            'query': 'The Big Lebowski',
            'year': '1998'
        }
        results = tmdb_service.search(kind='movie', **kwargs)
        assert len(results) == 2
        assert results[0]['title'] == 'The Big Lebowski'
        assert results[1]['title'] == 'The Making of \'The Big Lebowski\''

    def test_search__movie_title__non_unique(self, tmdb_service):
        kwargs = {
            'query': 'True Grit'
        }
        results = tmdb_service.search(kind='movie', **kwargs)
        # First 2 results are the original from 1969 and the 2010 remake.
        assert results[0]['title'] == 'True Grit'
        assert results[0]['release_date'] == '2010-12-22'
        assert results[1]['title'] == 'True Grit'
        assert results[1]['release_date'] == '1969-06-11'

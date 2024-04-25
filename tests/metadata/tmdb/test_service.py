import datetime
import os
import pytest

from media.movies.serializers import MovieSerializer
from media.shows.serializers import ShowSerializer, SeasonSerializer, EpisodeSerializer
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
        print(len(results))
        for movie in results:
            assert movie['release_date'] in ['2010-12-22', '1969-06-11', '1965-10-24', '1978-05-19', '1988-12-26', '2019-05-26']

    def test_retrieve_movie_metadata(self, tmdb_service):
        kwargs = {
            'query': 'The Big Lebowski',
            'year': '1998'
        }
        results = tmdb_service.search(kind='movie', **kwargs)
        movie_id = results[0].get('id')
        metadata = tmdb_service.retrieve_metadata(kind='movie', id=movie_id)
        metadata['filepath'] = os.path.abspath('tests/fixtures/samples/The Big Lebowski (1998).mp4')
        serializer = MovieSerializer(data=metadata)
        assert serializer.is_valid()
        assert serializer.validated_data.get('movie_rating') == 'R'
        assert serializer.validated_data.get('genres') == [{'name': 'Comedy'}, {'name': 'Crime'}]
        # There are just lots of credits
        assert len(serializer.validated_data.get('credits')) >= 167
        assert serializer.validated_data.get('credits')[0].get('name') == 'Jeff Bridges'
        assert serializer.validated_data.get('credits')[0].get('type') == 'cast'
        assert serializer.validated_data.get('credits')[0].get('role') == 'The Dude'

    def test_retrieve_show_metadata(self, tmdb_service):
        kwargs = {
            'query': 'Doug',
            'year': '1991'
        }
        results = tmdb_service.search(kind='tv', **kwargs)
        show_id = results[0].get('id')
        metadata = tmdb_service.retrieve_metadata(kind='tv', id=show_id)
        metadata['filepath'] = os.path.abspath('tests/fixtures/samples/Doug')
        serializer = ShowSerializer(data=metadata)
        assert serializer.is_valid()
        assert serializer.validated_data.get('genres') == [{'name': 'Animation'}, {'name': 'Comedy'}, {'name': 'Kids'}]

    def test_retrieve_season_metadata(self, tmdb_service, doug):
        kwargs = {
            'query': 'Doug',
            'year': '1991'
        }
        results = tmdb_service.search(kind='tv', **kwargs)
        show_id = results[0].get('id')
        metadata = tmdb_service.retrieve_metadata(kind='tv', id=show_id, season_num=1)
        metadata['filepath'] = os.path.abspath('tests/fixtures/samples/Doug/Season 01/01 - Doug Bags a Neematoad')
        serializer = SeasonSerializer(data=metadata)
        assert serializer.is_valid()
        assert serializer.validated_data.get('number') == 1
        assert serializer.validated_data.get('start_date') == datetime.date(1991, 8, 18)

    def test_retrieve_episode_metadata(self, tmdb_service, doug):
        kwargs = {
            'query': 'Doug',
            'year': '1991'
        }
        results = tmdb_service.search(kind='tv', **kwargs)
        show_id = results[0].get('id')
        metadata = tmdb_service.retrieve_metadata(kind='tv', id=show_id, season_num=1, episode_num=1)
        metadata['filepath'] = os.path.abspath('tests/fixtures/samples/Doug/Season 01/01 - Doug Bags a Neematoad')
        serializer = EpisodeSerializer(data=metadata)
        assert serializer.is_valid()
        assert serializer.validated_data.get('number') == 1
        assert serializer.validated_data.get('air_date') == datetime.date(1991, 8, 18)
        assert serializer.validated_data.get('title') == 'Doug Bags a Neematoad'

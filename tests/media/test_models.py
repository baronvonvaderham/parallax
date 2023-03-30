import os
import pytest

from media.exceptions import InvalidFilepathError
from media.movies.models import Movie, MovieManager
from media.movies.serializers import MovieSerializer


def test_retrieve_id(tmdb_service):
    kwargs = {
        'query': 'The Big Lebowski',
        'year': '1998'
    }
    id = tmdb_service.retrieve_id(kind='movie', **kwargs)
    assert id == 115


def test_title_year_from_file():
    filepath = os.path.abspath('tests/fixtures/samples/The Big Lebowski (1998).mp4')
    title, year = MovieManager._get_title_year_from_filepath(filepath=filepath)
    assert title == 'The Big Lebowski'
    assert year == '1998'


def test_title_year_from_file__no_year():
    filepath = os.path.abspath('tests/fixtures/samples/Not A Movie.crap')
    title, year = MovieManager._get_title_year_from_filepath(filepath=filepath)
    assert title == 'Not A Movie'
    assert year is None


def test_retrieve_metadata(tmdb_service, jeff_bridges):

    kwargs = {
        'query': 'The Big Lebowski',
        'year': '1998'
    }
    results = tmdb_service.search(kind='movie', **kwargs)
    movie_id = results[0].get('id')
    metadata = tmdb_service.retrieve_metadata(kind='movie', id=movie_id)
    serializer = MovieSerializer(data=metadata)
    assert serializer.is_valid()
    assert serializer.data.get('movie_rating') == 'R'
    assert serializer.data.get('genres') == [{'name': 'Comedy'}, {'name': 'Crime'}]
    # There are just lots of credits
    assert len(serializer.data.get('credits')) == 168
    assert serializer.data.get('credits')[0].get('name') == 'Jeff Bridges'
    assert serializer.data.get('credits')[0].get('type') == 'cast'
    assert serializer.data.get('credits')[0].get('role') == 'Jeffrey \'The Dude\' Lebowski'


def test_create_movie_with_metadata():
    filepath = os.path.abspath('tests/fixtures/samples/The Big Lebowski (1998).mp4')
    movie = Movie.objects.create_from_file(filepath)
    assert movie.genres.count() == 2
    assert movie.credits.count() == 168
    assert movie.title == 'The Big Lebowski'
    assert movie.sort_title == 'Big Lebowski, The'

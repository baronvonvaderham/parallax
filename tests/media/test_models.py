import datetime
import os
import pytest

from media.movies.models import Movie
from media.shows.models import Show, Season, Episode
from media.utils import get_title_year_from_filepath


def test_retrieve_id(tmdb_service):
    kwargs = {
        'query': 'The Big Lebowski',
        'year': '1998'
    }
    id = tmdb_service.retrieve_id(kind='movie', **kwargs)
    assert id == 115


def test_title_year_from_file():
    filepath = os.path.abspath('tests/fixtures/samples/The Big Lebowski (1998).mp4')
    title, year = get_title_year_from_filepath(filepath=filepath)
    assert title == 'The Big Lebowski'
    assert year == '1998'


def test_title_year_from_file__no_year():
    filepath = os.path.abspath('tests/fixtures/samples/Not A Movie.crap')
    title, year = get_title_year_from_filepath(filepath=filepath)
    assert title == 'Not A Movie'
    assert year is None


def test_create_movie_with_metadata():
    filepath = os.path.abspath('tests/fixtures/samples/The Big Lebowski (1998).mp4')
    movie = Movie.objects.create_from_file(filepath=filepath)
    assert movie.filepath == filepath
    assert movie.genres.count() == 2
    assert movie.credits.count() == 168
    assert movie.title == 'The Big Lebowski'
    assert movie.sort_title == 'Big Lebowski, The'


def test_create_show_with_metadata():
    filepath = os.path.abspath('tests/fixtures/samples/Doug')
    show = Show.objects.create_from_directory(filepath=filepath)
    assert show.filepath == filepath
    assert show.genres.count() == 3
    assert show.title == 'Doug'
    assert show.sort_title == 'Doug'
    assert show.tmdb_id == 384


def test_create_season_with_metatada(doug):
    season = Season.objects.create_season(season_number=1, show=doug)
    assert season.number == 1
    assert season.start_date == '1991-08-18'


def test_create_episode_with_metadata(doug, season1):
    episode = Episode.objects.create_episode(episode_number=1, season=season1)
    assert episode.number == 1
    assert episode.air_date == '1991-08-18'
    assert episode.title == 'Doug Bags a Neematoad'

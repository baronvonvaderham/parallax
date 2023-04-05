import os
import pytest


def test_movies_property(movie_library, big_lebowski):
    movie_library.movies.add(big_lebowski)
    assert movie_library.movies.count() == 1
    assert movie_library.movies.all()[0].title == 'The Big Lebowski'


def test_add_existing_movie(movie_library, big_lebowski):
    added = movie_library.add_existing_movie(big_lebowski)
    assert added


def test_add_movie_from_file(movie_library):
    filepath = os.path.abspath('tests/fixtures/samples/The Big Lebowski (1998).mp4')
    added = movie_library.add_movie_from_file(filepath=filepath)
    assert added


def test_add_show_from_directory(show_library):
    filepath = os.path.abspath('tests/fixtures/samples/Doug')
    added = show_library.add_new_show_from_directory(filepath=filepath)
    assert added
    shows = show_library.shows.all()
    assert len(shows) == 1
    doug = shows[0]
    assert doug.title == 'Doug'
    seasons = doug.seasons.all()
    assert len(seasons) == 2


def test_add_existing_show(show_library, doug):
    added = show_library.add_existing_show(doug)
    assert added

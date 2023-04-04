import pytest


def test_movies_property(movie_library, big_lebowski):
    movie_library.movies.add(big_lebowski)
    assert movie_library.movies.count() == 1
    assert movie_library.movies.all()[0].title == 'The Big Lebowski'

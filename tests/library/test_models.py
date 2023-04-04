import os
import pytest

from library.models import MovieLibrary
from media.movies.models import Movie


@pytest.mark.django_db(transaction=True)
def test_movies_property():
    movie_library = MovieLibrary.objects.create(name='MyMovies')
    filepath = os.path.abspath('tests/fixtures/samples/The Big Lebowski (1998).mp4')
    movie = Movie.objects.create_from_file(filepath=filepath)
    movie.library = movie_library
    movie.save()
    print(movie_library.movies.count())
    print(movie_library.movies.all())
    assert False

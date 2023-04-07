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
    """
    This is a full test of all parts of a show being added from just the input of its root filepath.
    It should automatically create the show, both associated seasons, and each episode in those season sub-folders.
    """
    filepath = os.path.abspath('tests/fixtures/samples/Doug')
    added = show_library.add_new_show_from_directory(filepath=filepath)
    assert added
    shows = show_library.shows.all()
    assert len(shows) == 1
    doug = shows[0]
    assert doug.title == 'Doug'
    seasons = doug.seasons.all()
    assert len(seasons) == 2
    for season in seasons:
        episodes = season.episodes.all()
        if season.number == 1:
            assert len(episodes) == 2
            if episodes[0].number == 1:
                assert episodes[0].title == 'Doug Bags a Neematoad'
            if episodes[0].number == 2:
                assert episodes[1].title == 'Doug Can\'t Dance'
        else:
            assert len(episodes) == 1
            assert episodes[0].title == 'Doug Takes the Case'
            assert episodes[0].number == 1


def test_add_existing_show(show_library, doug):
    added = show_library.add_existing_show(doug)
    assert added


def test_add_video_from_file(video_library):
    filepath = os.path.abspath('tests/fixtures/samples/My Home Movie.mp4')
    added = video_library.add_video_from_file(filepath=filepath)
    assert added

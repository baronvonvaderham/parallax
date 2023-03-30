import pytest


def test_retrieve_metadata(tmdb_service, jeff_bridges):
    from media.movies.serializers import MovieSerializer

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
    assert len(serializer.data.get('credits')) > 100
    assert serializer.data.get('credits')[0].get('name') == 'Jeff Bridges'
    assert serializer.data.get('credits')[0].get('type') == 'cast'
    assert serializer.data.get('credits')[0].get('role') == 'Jeffrey \'The Dude\' Lebowski'

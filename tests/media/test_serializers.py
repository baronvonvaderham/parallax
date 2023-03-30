import datetime
import pytest

from media.movies.serializers import MovieSerializer
from media.serializers import GenreSerializer, CreditSerializer, TagSerializer
from media.shows.serializers import ShowSerializer, SeasonSerializer, EpisodeSerializer
from media.videos.serializers import VideoSerializer


def test_genre_serializer(comedy):
    serializer = GenreSerializer(instance=comedy)
    assert serializer.data['name'] == 'Comedy'


def test_credit_serializer(jeff_bridges):
    serializer = CreditSerializer(instance=jeff_bridges)
    assert serializer.data['name'] == 'Jeff Bridges'
    assert serializer.data['role'] == 'The Dude'


def test_tag_serializer(classics):
    serializer = TagSerializer(instance=classics)
    assert serializer.data['name'] == 'Classics'


def test_movie_serializer(big_lebowski):
    serializer = MovieSerializer(instance=big_lebowski)
    assert serializer.data['title'] == 'The Big Lebowski'
    assert serializer.data['sort_title'] == 'Big Lebowski, The'
    assert not serializer.data['alternate_title']
    assert serializer.data['release_date'] == datetime.datetime(year=1998, month=3, day=6).date().isoformat()
    assert serializer.data['studio'] == ['Gramercy Pictures', 'PolyGram Filmed Entertainment', 'Working Title Films']
    assert serializer.data['movie_rating'] == 'R'
    summary = \
        """
        Jeff `The Dude' Leboswki is mistaken for Jeffrey Lebowski, who is The Big Lebowski. Which explains why he's 
        roughed up and has his precious rug peed on. In search of recompense, The Dude tracks down his namesake, 
        who offers him a job. His wife has been kidnapped and he needs a reliable bagman. Aided and hindered by 
        his pals Walter Sobchak, a Vietnam vet, and Donny, master of stupidity.
        """
    assert serializer.data['summary'] == summary
    assert len(serializer.data['genres']) == 2
    assert set([genre.get('name') for genre in serializer.data['genres']]) == {'Comedy', 'Crime'}
    assert set([credit.get('name') for credit in serializer.data['credits']]) == {'Jeff Bridges'}
    assert set([credit.get('role') for credit in serializer.data['credits']]) == {'The Dude'}
    assert set([tag.get('name') for tag in serializer.data['tags']]) == {'Classics', 'Stoner Movies'}


def test_show_serializer(doug):
    serializer = ShowSerializer(instance=doug)
    summary = \
        """
        The life of a young boy as he meets friends, falls in love, maneuvers his way through grade 6, 
        and writes all about it in his journal.
        """
    assert serializer.data['title'] == 'Doug'
    assert serializer.data['sort_title'] == 'Doug'
    assert not serializer.data['alternate_title']
    assert serializer.data['premiere_date'] == datetime.datetime(year=1991, month=8, day=11).date().isoformat()
    assert serializer.data['network'] == 'Nickelodeon'
    assert serializer.data['summary'] == summary
    assert set([genre.get('name') for genre in serializer.data['genres']]) == {'Comedy'}
    assert set([tag.get('name') for tag in serializer.data['tags']]) == {'Classics'}


def test_season_serializer(season1):
    serialzier = SeasonSerializer(instance=season1)
    assert serialzier.data['number'] == 1
    assert serialzier.data['start_date'] == datetime.datetime(year=1991, month=8, day=11).date().isoformat()
    assert serialzier.data['end_date'] == datetime.datetime(year=1991, month=12, day=8).date().isoformat()


def test_episode_serializer(doug_bags_a_neematoad):
    serializer = EpisodeSerializer(instance=doug_bags_a_neematoad)
    summary = \
    """
    Doug is new in Bluffington. When it seems all going well, the school bully, Roger Klotz, decides to 
    humiliate him after a ketchup incident. Roger then tells Doug to capture a nematoad, a popular mythical 
    and not real creature in Bluffington.
    """
    assert serializer.data['title'] == 'Doug Bags a Neematoad'
    assert serializer.data['air_date'] == datetime.datetime(year=1991, month=8, day=18).date().isoformat()
    assert serializer.data['tv_audience_label'] == 'TV-Y7'
    assert not serializer.data['tv_content_label']
    assert set([credit.get('name') for credit in serializer.data['credits']]) == {'Billy West'}
    assert set([credit.get('role') for credit in serializer.data['credits']]) == {'Douglas \'Doug\' Yancy Funnie'}


def test_video_serializer(video):
    serializer = VideoSerializer(instance=video)
    assert serializer.data['title'] == 'My First Birthday'
    assert serializer.data['release_date'] == datetime.datetime(year=1986, month=10, day=28).date().isoformat()
    assert serializer.data['summary'] == 'Video recorded as my first birthday!'

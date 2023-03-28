import datetime
import pytest

from core.serializers import UserSerializer
from library.serializers import (
    MovieLibrarySerializer,
    ShowLibrarySerializer,
    VideoLibrarySerializer,
)
from media.movies.serializers import MovieSerializer
from media.serializers import GenreSerializer, CreditSerializer, TagSerializer
from media.shows.serializers import ShowSerializer, SeasonSerializer, EpisodeSerializer
from media.videos.serializers import VideoSerializer
from server.constants import SERVER_DEFAULTS
from server.serializers import ServerSerializer


def test_user_serializer(user):
    serializer = UserSerializer(instance=user)
    assert serializer.data['email'] == 'feynman@caltech.edu'
    assert serializer.data['username'] == 'Feynman'


def test_server_serializer(server, user):
    serializer = ServerSerializer(instance=server)
    assert serializer.data['name'] == 'MyServer'
    assert serializer.data['remote_access']
    assert serializer.data['public_port'] == SERVER_DEFAULTS.get('PUBLIC_PORT')
    assert serializer.data['upload_limit'] == SERVER_DEFAULTS.get('UPLOAD_LIMIT')
    assert serializer.data['scan_automatically']
    assert serializer.data['changes_detected_scan']
    assert not serializer.data['scheduled_scan_enabled']
    assert serializer.data['scheduled_scan_interval'] == SERVER_DEFAULTS.get('SCHEDULED_SCAN_INTERVAL')
    assert serializer.data['empty_trash_after_scan']
    assert serializer.data['allow_delete']
    assert serializer.data['queue_retention_interval'] == SERVER_DEFAULTS.get('QUEUE_RETENTION_INTERVAL')
    assert serializer.data['max_queue_size'] == SERVER_DEFAULTS.get('MAX_QUEUE_SIZE')
    assert serializer.data['played_threshold'] == SERVER_DEFAULTS.get('PLAYED_THRESHOLD')
    assert serializer.data['paused_termination_limit'] == SERVER_DEFAULTS.get('PAUSED_TERMINATION_LIMIT')
    assert serializer.data['max_stream_count'] == SERVER_DEFAULTS.get('MAX_STREAM_COUNT')
    assert serializer.data['transcoding_enabled']
    assert serializer.data['max_transcode_count'] == SERVER_DEFAULTS.get('MAX_TRANSCODE_COUNT')
    assert serializer.data['owner'] == UserSerializer(instance=user).data
    assert not serializer.data['authorized_users']
    assert not serializer.data['preferred_language']


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


def test_movie_library_serializer(movie_library, server, user):
    serializer = MovieLibrarySerializer(instance=movie_library)
    assert serializer.data['name'] == movie_library.name
    assert not serializer.data['cover_photo']
    assert serializer.data['server'].get('name') == 'MyServer'


def test_show_library_serializer(show_library, server, user):
    serializer = ShowLibrarySerializer(instance=show_library)
    assert serializer.data['name'] == show_library.name
    assert not serializer.data['cover_photo']
    assert serializer.data['server'].get('name') == 'MyServer'


def test_video_library_serializer(video_library, server, user):
    serializer = VideoLibrarySerializer(instance=video_library)
    assert serializer.data['name'] == video_library.name
    assert not serializer.data['cover_photo']
    assert serializer.data['server'].get('name') == 'MyServer'


def test_movie_serializer(big_lebowski, movie_library):
    serializer = MovieSerializer(instance=big_lebowski)
    assert serializer.data['title'] == 'The Big Lebowski'
    assert serializer.data['sort_title'] == 'Big Lebowski, The'
    assert not serializer.data['alternate_title']
    assert serializer.data['release_date'] == datetime.datetime(year=1998, month=3, day=6).date().isoformat()
    assert serializer.data['studio'] == 'Working Title Films'
    assert serializer.data['movie_rating'] == 'R'
    summary = \
        """
        Jeff `The Dude' Leboswki is mistaken for Jeffrey Lebowski, who is The Big Lebowski. Which explains why he's 
        roughed up and has his precious rug peed on. In search of recompense, The Dude tracks down his namesake, 
        who offers him a job. His wife has been kidnapped and he needs a reliable bagman. Aided and hindered by 
        his pals Walter Sobchak, a Vietnam vet, and Donny, master of stupidity.
        """
    assert serializer.data['summary'] == summary
    assert serializer.data['library'].get('name') == movie_library.name
    assert serializer.data['library'].get('server').get('name') == 'MyServer'
    assert len(serializer.data['genres']) == 2
    assert set([genre.get('name') for genre in serializer.data['genres']]) == {'Comedy', 'Crime'}
    assert set([credit.get('name') for credit in serializer.data['credits']]) == {'Jeff Bridges'}
    assert set([credit.get('role') for credit in serializer.data['credits']]) == {'The Dude'}
    assert set([tag.get('name') for tag in serializer.data['tags']]) == {'Classics', 'Stoner Movies'}


def test_show_serializer(doug, show_library):
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
    assert serializer.data['library'].get('name') == show_library.name
    assert serializer.data['library'].get('server').get('name') == 'MyServer'
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


def test_video_serializer(video, video_library):
    serializer = VideoSerializer(instance=video)
    assert serializer.data['title'] == 'My First Birthday'
    assert serializer.data['release_date'] == datetime.datetime(year=1986, month=10, day=28).date().isoformat()
    assert serializer.data['summary'] == 'Video recorded as my first birthday!'
    assert serializer.data['library'].get('name') == video_library.name

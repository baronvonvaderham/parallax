from datetime import datetime
import pytest


@pytest.mark.django_db
@pytest.fixture
def create_genre():
    """
    A function to create 'media.Genre' instances.
    """
    from media.models import Genre

    def _create_genre(**kwargs):
        return Genre.objects.create(**kwargs)

    return _create_genre


@pytest.mark.django_db
@pytest.fixture
def comedy(create_genre):
    return create_genre(name='Comedy')


@pytest.mark.django_db
@pytest.fixture
def crime(create_genre):
    return create_genre(name='Crime')


@pytest.mark.django_db
@pytest.fixture
def create_credit():
    """
    A function to create 'media.Credit' instances.
    """
    from media.models import Credit

    def _create_credit(**kwargs):
        return Credit.objects.create(**kwargs)

    return _create_credit


@pytest.mark.django_db
@pytest.fixture
def jeff_bridges(create_credit):
    return create_credit(name='Jeff Bridges', role='The Dude')


@pytest.fixture
def billy_west(create_credit):
    return create_credit(name='Billy West', role='Douglas \'Doug\' Yancy Funnie')


@pytest.mark.django_db
@pytest.fixture
def create_tag():
    """
    A function to create 'media.Tag' instances.
    """
    from media.models import Tag

    def _create_tag(**kwargs):
        return Tag.objects.create(**kwargs)

    return _create_tag


@pytest.mark.django_db
@pytest.fixture
def classics(create_tag):
    return create_tag(name='Classics', description='Movies Ernest Cline has seen.')


@pytest.mark.django_db
@pytest.fixture
def stoner_movies(create_tag):
    return create_tag(name='Stoner Movies')


@pytest.mark.django_db
@pytest.fixture
def create_movie():
    """
    A function to create 'media.tmdb.Movie' instances.
    """
    from media.movies.models import Movie

    def _create_movie(**kwargs):
        return Movie.objects.create(**kwargs)

    return _create_movie


@pytest.mark.django_db
@pytest.fixture
def big_lebowski(create_movie, movie_library, comedy, crime, jeff_bridges, classics, stoner_movies):
    summary = \
        """
        Jeff `The Dude' Leboswki is mistaken for Jeffrey Lebowski, who is The Big Lebowski. Which explains why he's 
        roughed up and has his precious rug peed on. In search of recompense, The Dude tracks down his namesake, 
        who offers him a job. His wife has been kidnapped and he needs a reliable bagman. Aided and hindered by 
        his pals Walter Sobchak, a Vietnam vet, and Donny, master of stupidity.
        """
    kwargs = {
        'title': 'The Big Lebowski',
        'release_date': datetime(year=1998, month=3, day=6).date(),
        'studio': ['Gramercy Pictures', 'PolyGram Filmed Entertainment', 'Working Title Films'],
        'movie_rating': 'R',
        'tagline': 'They figured he was a lazy, time-wasting slacker. They were right. Her life was in their hands.',
        'summary': summary,
        'library': movie_library,
    }
    movie = create_movie(**kwargs)
    movie.genres.set([comedy, crime])
    movie.credits.set([jeff_bridges])
    movie.tags.set([classics, stoner_movies])
    return movie


@pytest.fixture
def create_show():
    """
    A function to create 'media.shows.Show' instances.
    """
    from media.shows.models import Show

    def _create_show(**kwargs):
        return Show.objects.create(**kwargs)

    return _create_show


@pytest.fixture
def doug(create_show, show_library, comedy, classics):
    summary = \
        """
        The life of a young boy as he meets friends, falls in love, maneuvers his way through grade 6, 
        and writes all about it in his journal.
        """
    kwargs = {
        'title': 'Doug',
        'premiere_date': datetime(year=1991, month=8, day=11).date(),
        'network': ['ABC', 'Nickelodeon'],
        'summary': summary,
        'library': show_library,
        'tmdb_id': 384,
    }
    show = create_show(**kwargs)
    show.genres.set([comedy])
    show.tags.set([classics])
    return show


@pytest.fixture
def create_season():
    """
    A function to create 'media.shows.Season' instances.
    """
    from media.shows.models import Season

    def _create_season(**kwargs):
        return Season.objects.create(**kwargs)

    return _create_season


@pytest.fixture
def season1(create_season, doug):
    kwargs = {
        'number': 1,
        'start_date': datetime(year=1991, month=8, day=11).date(),
        'end_date': datetime(year=1991, month=12, day=8).date(),
        'show': doug,
    }
    return create_season(**kwargs)


@pytest.fixture
def create_episode():
    """
    A function to create 'media.shows.Episode' instances.
    """
    from media.shows.models import Episode

    def _create_episode(**kwargs):
        return Episode.objects.create(**kwargs)

    return _create_episode


@pytest.fixture
def doug_bags_a_neematoad(create_episode, season1, doug, billy_west):
    summary = \
    """
    Doug is new in Bluffington. When it seems all going well, the school bully, Roger Klotz, decides to 
    humiliate him after a ketchup incident. Roger then tells Doug to capture a nematoad, a popular mythical 
    and not real creature in Bluffington.
    """
    kwargs = {
        'number': 2,
        'title': 'Doug Bags a Neematoad',
        'air_date': datetime(year=1991, month=8, day=18).date(),
        'tv_audience_label': 'TV-Y7',
        'season': season1
    }
    episode = create_episode(**kwargs)
    episode.credits.set([billy_west])
    return episode


@pytest.fixture
def create_video():
    """
    A function to create 'media.videos.Video' instances.
    """
    from media.videos.models import Video

    def _create_video(**kwargs):
        return Video.objects.create(**kwargs)

    return _create_video


@pytest.fixture
def video(create_video, video_library):
    kwargs = {
        'title': 'My First Birthday',
        'release_date': datetime(year=1986, month=10, day=28).date(),
        'summary': 'Video recorded as my first birthday!',
        'library': video_library,
    }
    return create_video(**kwargs)

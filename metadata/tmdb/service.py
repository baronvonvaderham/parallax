import json
import requests

from media.movies.constants import MOVIE_METADATA_FIELD_MAPPING
from media.shows.constants import (
    TV_METADATA_FIELD_MAPPING,
    SEASON_METADATA_FIELD_MAPPING,
    EPISODE_METADATA_FIELD_MAPPING,
)
from parallax import settings


class TheMovieDatabaseService(object):
    PATHS = {
        'search': '/search',
        'rating': '/certification',
    }
    KINDS = {
        'company': '/company',
        'collection': '/collection',
        'keyword': '/keyword',
        'movie': '/movie',
        'multi': '/multi',
        'person': '/person',
        'tv': '/tv',
    }
    MOVIE_LIST_FIELDS = [
        'studio',
        'country',
        'genres',
    ]
    TV_LIST_FIELDS = [
        'genres',
        'network',
    ]

    def __init__(self):
        self.api_key = settings.TMDB_V3_API_KEY
        self.request_headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }
        self.base_uri = 'https://api.themoviedb.org/3'

    def search(self, kind, **kwargs):
        """
        Method to perform a search query request.

        Kwargs:
            query: (required) The query string for the search being performed.
            year: The year of the item being searched for.
            primary_release_year: Narrower search parameter for year.
            page: The page of results to retrieve (Min: 1, Max: 1000, Default: 1
            include_adult: Allow pornographic results (default: True).
            region: ISO 3166-1 code to filter release dates.
        """
        path = self._get_path(method='search', kind=kind)
        kwargs['api_key'] = self.api_key
        response = self._get(uri=path, params=kwargs)
        results = json.loads(response.content).get('results')
        return results

    def retrieve_id(self, kind, **kwargs):
        """
        Method to retrieve the TMDB ID of an item.

        Kwargs:
            query: (required) The title of the item.
            year: The release date year of the item.
        """
        results = self.search(kind=kind, **kwargs)
        return results[0].get('id')

    def retrieve_metadata(self, kind, id, season_num=None, episode_num=None):
        """
        Method to retrieve full details of an item.
        """
        path = self._get_path(kind=kind, id=id)
        if kind == 'tv' and season_num and id:
            path += f'/season/{season_num}'
            if episode_num:
                path += f'/episode/{episode_num}?append_to_response=content_ratings'
        kwargs = {'api_key': self.api_key}
        response = self._get(uri=path, params=kwargs)
        if kind == 'movie':
            metadata = self._extract_movie_metadata(json.loads(response.content))
        elif kind == 'tv':
            if season_num:
                if episode_num:
                    metadata = self._extract_episode_metadata(json.loads(response.content))
                else:
                    metadata = self._extract_season_metadata(json.loads(response.content))
            else:
                metadata = self._extract_show_metadata(json.loads(response.content))
        else:
            return None
        return metadata

    def retrieve_credits(self, kind, id):
        """
        Method to retrieve the credits associated wth an item.
        """
        path = self._get_path(kind=kind, id=id, method='credits')
        kwargs = {'api_key': self.api_key}
        response = self._get(uri=path, params=kwargs)
        return self._extract_credits(json.loads(response.content))

    def _get(self, uri, params):
        """
        Method to execute get request against TMDB endpoint.
        """
        return requests.get(uri, params=params, headers=self.request_headers)

    def _get_path(self, kind, method=None, id=None):
        """
        Method to construct the URI of the endpoint against which the query is being run.
        """
        uri = self.base_uri
        if self.PATHS.get(method):
            uri += self.PATHS.get(method)
        if self.KINDS.get(kind):
            uri += self.KINDS.get(kind)
        if id:
            uri += f'/{id}'
        if not method and kind == 'movie':
            # Necessary to get the MPAA rating which is only included in the /release_dates response data.
            # Appending it here allows us to only make one API call for all data.
            uri += '?append_to_response=release_dates'
        if method == 'credits':
            uri += '/credits'
        return uri

    def _extract_movie_metadata(self, data):
        """
        Helper method to map TMDB movie data to model attributes here.
        """
        metadata = {}
        for field in MOVIE_METADATA_FIELD_MAPPING.keys():
            if field in self.MOVIE_LIST_FIELDS and data.get(MOVIE_METADATA_FIELD_MAPPING[field]):
                if field == 'country':
                    d = [item.get('iso_3166_1') for item in data.get(MOVIE_METADATA_FIELD_MAPPING[field])]
                else:
                    d = [item.get('name') for item in data.get(MOVIE_METADATA_FIELD_MAPPING[field])]
                metadata[field] = d
            else:
                metadata[field] = data.get(MOVIE_METADATA_FIELD_MAPPING[field])
        metadata = self._append_rating(metadata, data)
        metadata = self._append_genres(metadata, data)
        metadata = self._append_credits(metadata, data)
        return metadata

    def _extract_show_metadata(self, data):
        """
        Helper method to map TMDB tv show data to model attributes here.
        """
        metadata = {}
        for field in TV_METADATA_FIELD_MAPPING.keys():
            if field in self.TV_LIST_FIELDS and data.get(TV_METADATA_FIELD_MAPPING[field]):
                d = [item.get('name') for item in data.get(TV_METADATA_FIELD_MAPPING[field])]
                metadata[field] = d
            else:
                metadata[field] = data.get(TV_METADATA_FIELD_MAPPING[field])
        metadata = self._append_genres(metadata, data)
        return metadata

    @staticmethod
    def _extract_season_metadata(data):
        """
        Helper method to map TMDB tv season data to model attributes here.
        """
        metadata = {}
        for field in SEASON_METADATA_FIELD_MAPPING.keys():
            metadata[field] = data.get(SEASON_METADATA_FIELD_MAPPING[field])
        return metadata

    @staticmethod
    def _extract_episode_metadata(data):
        """
        Helper Method to map TMDB tv episode data to model attributes here.
        """
        metadata = {}
        for field in EPISODE_METADATA_FIELD_MAPPING.keys():
            metadata[field] = data.get(EPISODE_METADATA_FIELD_MAPPING[field])
        return metadata

    @staticmethod
    def _extract_credits(data):
        """
        Helper method to extract Credits out of the TMDB response data.
        """
        credits = []
        for member in data.get('cast'):
            credits.append({'name': member.get('name'), 'role': member.get('character'), 'type': 'cast'})
        # for member in data.get('crew'):
        #     credits.append({'name': member.get('name'), 'role': member.get('job'), 'type': 'crew'})
        return credits

    @staticmethod
    def _append_rating(metadata, data):
        """
        Helper method to extract MPAA rating values from TMDB's response data and append
        it to the metadata dict used to create models here.
        """
        results = data.get('release_dates').get('results')
        rating = None
        for result in results:
            if result.get('iso_3166_1') == 'US':
                rating = result.get('release_dates')[0].get('certification')
        metadata['movie_rating'] = rating
        return metadata

    @staticmethod
    def _append_genres(metadata, data):
        """
        Helper method to extract Genre values and place them in the correct location
        within the metadata dict used to create models here.
        """
        genres = [{'name': genre.get('name')} for genre in data.get('genres')]
        metadata['genres'] = genres
        return metadata

    def _append_credits(self, metadata, data):
        """
        Helper method to put the list of credits extracted in self._extract_credits() into a usable
        form in the correct location within the metadata dict used to create models here.
        """
        credits = self.retrieve_credits(kind='movie', id=data.get('id'))
        metadata['credits'] = credits
        return metadata

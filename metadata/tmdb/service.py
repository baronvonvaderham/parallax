import json
import requests

from media.movies.constants import MOVIE_METADATA_FIELD_MAPPING
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
    LIST_FIELDS = [
        'studio',
        'country',
        'genres',
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

    def retrieve_metadata(self, kind, id):
        """
        Method to retrieve full details of an item.
        """
        path = self._get_path(kind=kind, id=id)
        kwargs = {'api_key': self.api_key}
        response = self._get(uri=path, params=kwargs)
        return self._extract_metadata(json.loads(response.content))

    def retrieve_credits(self, kind, id):
        path = self._get_path(kind=kind, id=id, method='credits')
        kwargs = {'api_key': self.api_key}
        response = self._get(uri=path, params=kwargs)
        return self._extract_credits(json.loads(response.content))

    def _get(self, uri, params):
        return requests.get(uri, params=params, headers=self.request_headers)

    def _get_path(self, kind, method=None, id=None):
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

    def _extract_metadata(self, data):
        metadata = {}
        for field in MOVIE_METADATA_FIELD_MAPPING.keys():
            if field in self.LIST_FIELDS:
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

    @staticmethod
    def _extract_credits(data):
        credits = []
        for member in data.get('cast'):
            credits.append({'name': member.get('name'), 'role': member.get('character'), 'type': 'cast'})
        for member in data.get('crew'):
            credits.append({'name': member.get('name'), 'role': member.get('job'), 'type': 'crew'})
        return credits

    @staticmethod
    def _append_rating(metadata, data):
        results = data.get('release_dates').get('results')
        rating = None
        for result in results:
            if result.get('iso_3166_1') == 'US':
                rating = result.get('release_dates')[0].get('certification')
        metadata['movie_rating'] = rating
        return metadata

    @staticmethod
    def _append_genres(metadata, data):
        genres = [{'name': genre.get('name')} for genre in data.get('genres')]
        metadata['genres'] = genres
        return metadata

    def _append_credits(self, metadata, data):
        credits = self.retrieve_credits(kind='movie', id=data.get('id'))
        metadata['credits'] = credits
        return metadata

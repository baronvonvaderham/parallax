import json
import requests

from parallax import settings


class TheMovieDatabaseService(object):
    PATHS = {
        'search': '/search'
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

    def _get_path(self, method, kind):
        return self.base_uri + self.PATHS.get(method) + self.KINDS.get(kind)

    def _get(self, uri, params):
        return requests.get(uri, params=params, headers=self.request_headers)

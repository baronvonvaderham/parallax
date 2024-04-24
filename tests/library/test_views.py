import pytest

from rest_framework.test import APIClient


# @pytest.mark.django_db
# def test_library_list_view(user, movie_library, show_library):
#     user.movielibrary_set.add(movie_library)
#     user.showlibrary_set.add(show_library)
#
#     token = user.oauth2_provider_accesstoken.create()
#     client = APIClient()
#     client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
#
#     response = client.get('/library/list/')
#     print(response)
#     assert False

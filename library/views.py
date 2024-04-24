from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User


class LibraryListView(APIView):

    def get(self, request):
        user = User.objects.get(email=request.user.email)
        data = {
            'movie_libraries': user.movielibraries.all(),
            'show_libraries': user.showlibraries.all(),
            'video_libraries': user.videolibraries.all(),
        }
        return Response(data)

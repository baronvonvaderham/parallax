from rest_framework.views import APIView
from rest_framework.response import Response

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

from rest_framework import serializers

from library.models import MovieLibrary, ShowLibrary, VideoLibrary
from server.serializers import ServerSerializer


class LibrarySerializer(object):
    name = serializers.CharField(required=True, max_length=128)
    cover_photo = serializers.CharField(required=False, allow_blank=True, max_length=128)
    server = ServerSerializer()


class MovieLibrarySerializer(LibrarySerializer):

    class Meta:
        model = MovieLibrary
        fields = []


class ShowLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowLibrary
        fields = []


class VideoLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoLibrary
        fields = []

from rest_framework import serializers

from library.models import MovieLibrary, ShowLibrary, VideoLibrary
from server.serializers import ServerSerializer


class LibrarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=128)
    cover_photo = serializers.CharField(required=False, allow_blank=True, max_length=128)
    server = ServerSerializer()


class MovieLibrarySerializer(LibrarySerializer):

    class Meta:
        model = MovieLibrary
        fields = ['name', 'cover_photo', 'server']


class ShowLibrarySerializer(LibrarySerializer):

    class Meta:
        model = ShowLibrary
        fields = ['name', 'cover_photo', 'server']


class VideoLibrarySerializer(LibrarySerializer):

    class Meta:
        model = VideoLibrary
        fields = ['name', 'cover_photo', 'server']

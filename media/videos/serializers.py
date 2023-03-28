from rest_framework import serializers

from library.serializers import VideoLibrarySerializer
from media.videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=256)
    sort_title = serializers.CharField(required=True, max_length=256)
    release_date = serializers.DateField(required=False, allow_null=True)
    summary = serializers.CharField(required=False, allow_null=True)
    poster_image = serializers.CharField(required=False, max_length=128, allow_null=True)
    country = serializers.CharField(required=False, max_length=8, allow_null=True)

    library = VideoLibrarySerializer()

    class Meta:
        model = Video
        fields = ['title', 'sort_title', 'release_date', 'summary', 'poster_image', 'country', 'library']

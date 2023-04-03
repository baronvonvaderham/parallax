from rest_framework import serializers

from media.videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    filepath = serializers.CharField(required=True, max_length=1024)
    title = serializers.CharField(required=True, max_length=256)
    sort_title = serializers.CharField(required=True, max_length=256)
    release_date = serializers.DateField(required=False, allow_null=True)
    summary = serializers.CharField(required=False, allow_null=True)
    poster_image = serializers.CharField(required=False, max_length=128, allow_null=True)
    country = serializers.ListField(child=serializers.CharField(max_length=8), required=False, allow_null=True)

    class Meta:
        model = Video
        fields = ['filepath', 'title', 'sort_title', 'release_date', 'summary', 'poster_image', 'country']

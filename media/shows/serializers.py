from rest_framework import serializers

from library.serializers import ShowLibrarySerializer
from media.serializers import GenreSerializer, TagSerializer, CreditSerializer
from media.shows.constants import TV_AUDIENCE_LABEL, TV_CONTENT_LABEL
from media.shows.models import Show, Season, Episode


class EpisodeSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(required=True)
    title = serializers.CharField(required=False, max_length=256, allow_null=True)
    air_date = serializers.DateField(required=False, allow_null=True)
    tv_audience_label = serializers.ChoiceField(choices=TV_AUDIENCE_LABEL, required=False, allow_null=True)
    tv_content_label = serializers.ChoiceField(choices=TV_CONTENT_LABEL, required=False, allow_null=True)
    poster_image = serializers.CharField(required=False, max_length=128, allow_null=True)

    credits = CreditSerializer(many=True)

    class Meta:
        model = Episode
        fields = ['number', 'title', 'air_date', 'tv_audience_label', 'tv_content_label', 'poster_image', 'credits']


class SeasonSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(required=True)
    start_date = serializers.DateField(required=False, allow_null=True)
    end_date = serializers.DateField(required=False, allow_null=True)
    poster_image = serializers.CharField(required=False, max_length=128, allow_null=True)

    class Meta:
        model = Season
        fields = ['number', 'start_date', 'end_date', 'poster_image']


class ShowSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=256)
    sort_title = serializers.CharField(required=False, max_length=256, allow_null=True)
    alternate_title = serializers.CharField(required=False, max_length=256, allow_null=True)
    premiere_date = serializers.DateField(required=False, allow_null=True)
    network = serializers.CharField(required=False, max_length=56, allow_null=True)
    summary = serializers.CharField(required=False, allow_null=True)
    poster_image = serializers.CharField(required=False, max_length=128, allow_null=True)
    country = serializers.CharField(required=False, max_length=8, allow_null=True)

    library = ShowLibrarySerializer()
    genres = GenreSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Show
        fields = ['title', 'sort_title', 'alternate_title', 'premiere_date', 'network', 'summary',
                  'poster_image', 'country', 'library', 'genres', 'tags']

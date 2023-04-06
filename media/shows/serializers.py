from rest_framework import serializers

from media.serializers import GenreSerializer, TagSerializer, CreditSerializer
from media.shows.constants import TV_AUDIENCE_LABEL, TV_CONTENT_LABEL
from media.shows.models import Show, Season, Episode


class EpisodeSerializer(serializers.ModelSerializer):
    filepath = serializers.CharField(required=True, max_length=1024)
    number = serializers.IntegerField(required=True)
    title = serializers.CharField(required=False, max_length=256, allow_null=True)
    air_date = serializers.DateField(required=False, allow_null=True)
    tv_audience_label = serializers.ChoiceField(choices=TV_AUDIENCE_LABEL, required=False, allow_null=True)
    tv_content_label = serializers.ChoiceField(choices=TV_CONTENT_LABEL, required=False, allow_null=True)
    poster_image = serializers.CharField(required=False, max_length=128, allow_null=True)

    credits = CreditSerializer(many=True, required=False)

    class Meta:
        model = Episode
        fields = ['filepath', 'number', 'title', 'air_date', 'tv_audience_label', 'tv_content_label',
                  'poster_image', 'credits']


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
    network = serializers.ListField(child=serializers.CharField(max_length=56), required=False,  allow_null=True)
    summary = serializers.CharField(required=False, allow_null=True)
    poster_image = serializers.CharField(required=False, max_length=128, allow_null=True)
    country = serializers.ListField(child=serializers.CharField(max_length=8), required=False, allow_null=True)
    tmdb_id = serializers.IntegerField(required=False, allow_null=False)

    genres = GenreSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Show
        fields = ['title', 'sort_title', 'alternate_title', 'premiere_date', 'network', 'summary',
                  'poster_image', 'country', 'tmdb_id', 'genres', 'tags']

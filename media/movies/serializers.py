from rest_framework import serializers

from media.serializers import GenreSerializer, CreditSerializer, TagSerializer
from media.movies.constants import MOVIE_RATINGS
from media.movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=256)
    sort_title = serializers.CharField(required=False, max_length=256, allow_null=True)
    alternate_title = serializers.CharField(required=False, max_length=256, allow_null=True)
    release_date = serializers.DateField(required=False, allow_null=True)
    studio = serializers.ListField(child=serializers.CharField(max_length=128), required=False, allow_null=True)
    movie_rating = serializers.ChoiceField(choices=MOVIE_RATINGS, required=False, allow_null=True)
    tagline = serializers.CharField(required=False, allow_null=True)
    summary = serializers.CharField(required=False, allow_null=True)
    poster_image = serializers.CharField(required=False, max_length=128, allow_null=True)
    country = serializers.ListField(child=serializers.CharField(max_length=8), required=False, allow_null=True)

    genres = GenreSerializer(many=True, required=False)
    credits = CreditSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = ['title', 'sort_title', 'alternate_title', 'release_date', 'studio', 'movie_rating',
                  'tagline', 'summary', 'poster_image', 'country', 'genres', 'credits', 'tags']

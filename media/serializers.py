from rest_framework import serializers

from media.models import Genre, Credit, Tag


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=32)

    class Meta:
        model = Genre
        fields = ['name']


class CreditSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=128)
    role = serializers.CharField(required=True, max_length=128)

    class Meta:
        model = Credit
        fields = ['name', 'role']


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=128)

    class Meta:
        model = Tag
        fields = ['name']

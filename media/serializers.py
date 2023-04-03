from rest_framework import serializers

from media.constants import CREDIT_TYPES
from media.models import Genre, Credit, Tag


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=32)

    class Meta:
        model = Genre
        fields = ['name']


class CreditSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=128)
    role = serializers.CharField(required=True, max_length=128)
    type = serializers.ChoiceField(choices=CREDIT_TYPES, required=True)

    class Meta:
        model = Credit
        fields = ['name', 'role', 'type']


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=128)
    description = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Tag
        fields = ['name', 'description']

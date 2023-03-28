from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=28)

    class Meta:
        model = User
        fields = ['email', 'username']

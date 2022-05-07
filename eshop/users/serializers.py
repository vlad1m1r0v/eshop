from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar = serializers.ImageField(
        allow_empty_file=True, use_url=True, required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

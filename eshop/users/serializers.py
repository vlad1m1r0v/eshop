from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile, UserAddress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserAddressSerializer(serializers.ModelSerializer):
    country = serializers.CharField(required=True, max_length=15, min_length=3)
    region = serializers.CharField(required=True, max_length=15, min_length=3)
    city = serializers.CharField(required=True, max_length=15, min_length=3)
    street = serializers.CharField(required=True, max_length=15, min_length=3)
    zip_code = serializers.IntegerField(required=True)

    class Meta:
        model = UserAddress
        exclude = ('user_profile', )


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar = serializers.ImageField(
        allow_empty_file=True, use_url=True, required=False)

    class Meta:
        model = UserProfile
        fields = '__all__'

    # flatten nested user
    def to_representation(self, obj):
        representation = super().to_representation(obj)
        user_representation = representation.pop('user')
        for key in user_representation:
            representation[key] = user_representation[key]

        return representation

    def to_internal_value(self, data):
        user_internal = {}

        for key in UserSerializer.Meta.fields:
            if key in data:
                user_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal['user'] = user_internal
        return internal

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        super().update(instance, validated_data)

        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        return instance

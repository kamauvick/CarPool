from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Location, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('auth_token', 'refresh_token',)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']


class LocationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=60)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('title', instance.title)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)

        instance.save()
        return instance

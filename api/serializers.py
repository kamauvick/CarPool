import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Location, Profile, Trip_Offers, Trip_Request, Trip


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', ]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('phone_number', 'auth_token', 'user')


class LocationSerializer(serializers.Serializer):
    location_id = serializers.IntegerField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    def create(self, validated_data):
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.location_id = validated_data.get('location_id', instance.location_id)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.latitude = validated_data.get('latitude', instance.latitude)

        instance.save()
        return instance


class TripOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip_Offers
        exclude = ()

    def create(self, validated_data):
        return Trip_Offers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.driver = validated_data.get('driver', instance.driver)
        instance.departure_time = validated_data.get('departure_time', instance.departure_time)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.available_seats = validated_data.get('available_seats', instance.available_seats)
        instance.destination = validated_data.get('destination', instance.destination)
        instance.is_complete = validated_data.get('is_complete', instance.is_complete)


class TripRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip_Request
        fields = ('departure_time', 'origin', 'destination')

    def create(self, validated_data):
        return Trip_Request.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.departure_time = validated_data.get('departure_time', instance.departure_time)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.destination = validated_data.get('destination', instance.destination)


class TripSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        driver = self.context["request"].user.profile
        validated_data['driver'] = driver
        validated_data['date'] = datetime.date.today()
        return super().create(validated_data)

    class Meta:
        model = Trip
        fields = ["id", "departure_time", "arrival_time", "destination", "driver", "is_complete", "origin",
                  "available_seats", "date", 'created_at']
        read_only_fields = ["driver", "created_at", "date"]

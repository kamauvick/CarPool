import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Location, Profile, Trip, Trip_Request


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        raise ValidationError(detail='not supported')

    def update(self, instance, validated_data):
        if self.context['request'].user != instance.user:
            raise ValidationError(detail='Must be user to edit')
        phone_number = validated_data.get('phone_number', None)
        if phone_number is None:
            if not self.partial:
                raise ValidationError(detail='Phone number must be provided')
        else:
            instance.phone_number = phone_number
            instance.save()
        return instance

    class Meta:
        model = Profile
        fields = ('id', 'phone_number', "profile_pic", 'user',)


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


class TripSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        driver = self.context["request"].user.profile
        validated_data['driver'] = driver
        validated_data['date'] = datetime.date.today()
        return super().create(validated_data)

    class Meta:
        model = Trip
        fields = ["id", "departure_time", "arrival_time", "destination", "driver", "is_complete", "origin",
                  "available_seats", "date", 'created_at', "available_seats"]
        read_only_fields = ["driver", "created_at", "date", "is_complete", "origin"]


class TripRequestSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        trip: Trip = validated_data['trip']

        count = len(trip.trip_requests.all())
        if count >= trip.available_seats or trip.full:
            raise ValidationError(detail="Trip is full")
        passenger = self.context['request'].user.profile
        if trip.trip_requests.filter(passenger=passenger):
            raise ValidationError(detail="Already booked trip")

        if trip.driver == passenger:
            raise ValidationError(detail='Driver cannot book a seat')
        validated_data['passenger'] = passenger
        r = Trip_Request.objects.create(**validated_data)
        return r

    def update(self, instance, validated_data):
        raise ValidationError(detail="not implemented")

    class Meta:
        model = Trip_Request
        fields = ["id", "trip", "passenger", "accepted"]
        read_only_fields = ["passenger", "accepted"]

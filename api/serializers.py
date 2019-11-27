import datetime

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Profile, Trip, Trip_Request


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
        print(phone_number)
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


class TripSerializer(serializers.ModelSerializer):
    driver = ProfileSerializer(read_only=True)
    requests = serializers.SerializerMethodField()

    def get_requests(self, obj):
        return TripRequestSerializer(obj.trip_requests.all(), many=True).data

    def create(self, validated_data):
        driver = self.context["request"].user.profile
        validated_data['driver'] = driver
        validated_data['date'] = datetime.date.today()
        return super().create(validated_data)

    class Meta:
        model = Trip
        fields = ["id", "departure_time", "arrival_time", "destination", "driver", "status", "origin",
                  "available_seats", 'requests', "date", 'created_at', ]

        read_only_fields = ["driver", "created_at", "date", 'requests']


class TripRequestSerializer(serializers.ModelSerializer):
    passenger = ProfileSerializer(read_only=True)
    driver = ProfileSerializer(read_only=True)

    my_trip = TripSerializer(read_only=True)

    def create(self, validated_data):
        trip: Trip = validated_data['trip']

        count = len(trip.trip_requests.all())
        if count >= trip.available_seats or trip.full:
            raise ValidationError(detail="The trip is full..please check another one :)")
        passenger = self.context['request'].user.profile
        if trip.trip_requests.filter(passenger=passenger):
            raise ValidationError(detail="You've already booked that trip")

        if trip.driver == passenger:
            raise ValidationError(detail='The driver who created the offer cannot book a seat')
        validated_data['passenger'] = passenger
        r = Trip_Request.objects.create(**validated_data)
        return r

    class Meta:
        model = Trip_Request
        fields = ["id", "trip", "passenger", "driver", "accepted", "my_trip", ]
        read_only_fields = ["passenger", "driver", "my_trip", ]

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    auth_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        db_table = 'users'


class Location(models.Model):
    name = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'locations'
        ordering = ['-name']


class Trip(models.Model):
    driver = models.ForeignKey(Profile, on_delete=models.PROTECT)
    departure_time = models.DateTimeField(auto_now_add=True)
    available_seats = models.PositiveSmallIntegerField()
    complete = models.BooleanField(default=False)
    arrival_time = models.DateTimeField()

    def __str__(self):
        return f'{self.driver}'

    class Meta:
        db_table = 'trips'
        ordering = ['-departure_time']


class Trip_Passenger(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    passenger = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.passenger}'

    class Meta:
        db_table = 'trip_passenger'
        ordering = ['-trip']


class Trip_Requests(models.Model):
    request = models.ForeignKey(Trip_Passenger, on_delete=models.PROTECT)
    passenger = models.ForeignKey(Profile, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.request}'

    class Meta:
        db_table = 'trip-requests'
        ordering = ['-request']

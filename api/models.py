from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=100)
    auth_token = models.CharField(max_length=200)

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


class Trip(models.Model):
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    departure_time = models.TimeField()
    available_seats = models.IntegerField()
    driver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    arrival_time = models.TimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.origin}'

    class Meta:
        db_table = 'trips'
        ordering = ['-departure_time']


class Trip_Request(models.Model):
    trip = models.ForeignKey('api.Trip', related_name='trip_requests', on_delete=models.PROTECT)
    passenger = models.ForeignKey('api.Profile', related_name='trip_passengers', on_delete=models.PROTECT)
    accepted = models.BooleanField(default=False)

    # def __str__(self):
    #     return f'Trip Name:{self.destination}'

    class Meta:
        verbose_name = 'triprequest'
        db_table = 'trip_request'
        # ordering = ['-destination']


class Trip_Offers(models.Model):
    driver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    start_time = models.TimeField()
    destination = models.CharField(max_length=200)
    available_seats = models.IntegerField()
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'Offer id:{self.driver}'

    @classmethod
    def get_offer_by_destination(cls, destination, time):
        offers = cls.objects.filter(cls(destination__icontains=destination) | cls(departure_time__icontains=time))
        return offers

    class Meta:
        verbose_name = 'tripoffers'
        db_table = 'trip-offers'
        ordering = ['-driver']


class Location(models.Model):
    location_id = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    request = models.ForeignKey(Trip_Request, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.longitude} : {self.latitude}'

    class Meta:
        db_table = 'locations'
        ordering = ['-location_id']


class RequestBoard(models.Model):
    request = models.ForeignKey(Trip_Request, on_delete=models.CASCADE)
    is_complete = models.BooleanField()

    class Meta:
        db_table = 'requestBoard'

    def __str__(self):
        return f'{self.request}'

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, default='sample.jpg')
    phone_number = models.CharField(max_length=100)

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
    REQUESTED = 'REQUESTED'
    STARTED = 'STARTED'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

    STATUSES = (
        (REQUESTED, REQUESTED),
        (STARTED, STARTED),
        (IN_PROGRESS, IN_PROGRESS),
        (COMPLETED, COMPLETED),
    )

    status = models.CharField(max_length=20,
                              choices=STATUSES,
                              default=REQUESTED)
    origin = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    departure_time = models.TimeField()
    available_seats = models.IntegerField()
    driver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    arrival_time = models.TimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    full = models.BooleanField(default=False)
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

    def __str__(self):
        return f'Trip Name:{self.passenger}'

    class Meta:
        verbose_name = 'triprequest'
        db_table = 'trip_request'


class Trip_Offers(models.Model):
    trip = models.ForeignKey('api.Trip', related_name='trip_offers', on_delete=models.PROTECT)
    driver = models.ForeignKey('api.Profile', related_name='trip_driver', on_delete=models.CASCADE)

    def __str__(self):
        return f'Offer id:{self.driver}'

    class Meta:
        verbose_name = 'tripoffers'
        db_table = 'trip-offers'


class RequestBoard(models.Model):
    request = models.ForeignKey(Trip_Request, on_delete=models.CASCADE, related_name='request')

    # @receiver(post_save, sender=Trip_Request)
    # def create_trip(sender, instance, created, **kwargs):
    #     if created:
    #         RequestBoard.objects.create(request=instance)
    #
    # @receiver(post_save, sender=Trip_Request)
    # def save_trip(sender, instance, **kwargs):
    #     instance.request.save()

    class Meta:
        db_table = 'requestBoard'

    def __str__(self):
        return f'{self.request}'

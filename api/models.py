from django.db import models


# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    auth_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        db_table = 'users'
        ordering = ['-first_name']


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
    driver = models.ForeignKey(Users, on_delete=models.PROTECT)
    departure_time = models.DateTimeField(auto_now_add=True)
    available_seats = models.PositiveSmallIntegerField()
    complete = models.BooleanField(default=False)
    stop = models.DateTimeField()

    def __str__(self):
        return f'{self.driver}'

    class Meta:
        db_table = 'trips'
        ordering = ['-departure_time']


class Trip_passenger(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    passenger = models.ForeignKey(Users, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.passenger}'

    class Meta:
        db_table = 'trip_passenger'
        ordering = ['-trip']


class Trip_Requests(models.Model):
    request = models.ForeignKey(Trip_passenger, on_delete=models.PROTECT)
    passenger = models.ForeignKey(Users, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.request}'

    class Meta:
        db_table = 'trip-requests'
        ordering = ['-request']

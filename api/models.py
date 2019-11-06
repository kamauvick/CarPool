from django.db import models


# Create your models here.
class Users(models.Model):
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    auth_token = models.CharField(max_length=256)
    restart_token = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'
        ordering = ['-f_name']


class Location(models.Model):
    pass


class Trip(models.Model):
    pass


class Trip_passenger(models.Model):
    pass


class Trip_Requests(models.Model):
    pass

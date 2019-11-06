from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    auth_token = models.CharField(max_length=256)
    restart_token = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users'

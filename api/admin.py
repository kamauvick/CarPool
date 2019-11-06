from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Users)
admin.site.register(Location)
admin.site.register(Trip)
admin.site.register(Trip_passenger)
admin.site.register(Trip_Requests)
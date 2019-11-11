from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Trip)
admin.site.register(Trip_Request)
admin.site.register(Trip_Offers)

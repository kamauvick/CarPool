from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Trip_Request)
admin.site.register(Trip_Offers)


@admin.register(Trip)
class Trip(admin.ModelAdmin):
    exclude = ('',)

    list_display = ("id",
                    "departure_time", "arrival_time", "destination", "driver", "status", "origin",
                    "available_seats", "date", 'created_at',)

    list_filter = (
        'status',
        'destination',
        'departure_time',
    )

    ordering = ("-departure_time",)

    read_only_fields = ("driver", "created_at", "date", "origin",)

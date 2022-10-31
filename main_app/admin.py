from django.contrib import admin
from .models import Trip, Itinerary, Activity

# Register your models here.
admin.site.register(Trip)
admin.site.register(Itinerary)
admin.site.register(Activity)
from django.contrib import admin
from .models import Trip, Itinerary, Activity, Photo

# Register your models here.
admin.site.register(Trip)
admin.site.register(Itinerary)
admin.site.register(Activity)
admin.site.register(Photo)
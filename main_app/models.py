from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Trip(models.Model):
    trip_name = models.CharField(max_length=100)
    locations = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.trip_name} ({self.id})"

    #for when we implement our CBV
    def get_absolute_url(self):
        return reverse("detail", kwargs={"trip_id": self.id})

class Itinerary(models.Model):
    date = models.DateField()
    # connect to Trip model
    trip = models.ForeignKey(
    Trip,
    on_delete=models.CASCADE
    )
    notes = models.TextField(max_length=250)
    def __str__(self):
        return f"{self.date}"

    #for when we implement our CBV
    def get_absolute_url(self):
        return reverse("itineraries_detail", kwargs={"itinerary_id": self.id})

    class Meta:
        ordering = ["-date"]
        
               
class Activity(models.Model):
    activity_name = models.CharField(max_length=100)
    time = models.TimeField('Time Slot')
    locations = models.TextField(max_length=250)
    # connect to Itinerary model
    itinerary = models.ForeignKey(
        Itinerary,
    on_delete=models.CASCADE
    )
    def __str__(self):
        return f"{self.activity_name}"

    #for when we implement our CBV
    def get_absolute_url(self):
        return reverse("activities_detail", kwargs={"activity_id": self.id})

    class Meta:
        ordering = ["-time"]

class Photo(models.Model):
    url = models.CharField(max_length=200)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return f"Activity ID {self.activity_id} @{self.url}"

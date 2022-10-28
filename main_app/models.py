from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Trip(models.Model):
    trip_name = models.CharField(max_length=100)
    locations = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.id})"

    #for when we implement our CBV
    def get_absolute_url(self):
        return reverse("detail", kwargs={"trip_id": self.id})
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trip(models.Model):
    name = models.CharField(max_length=100)
    locations = models.TextField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
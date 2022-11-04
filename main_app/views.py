from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Trip, Itinerary, Activity, Photo
from .forms import ItineraryForm, ActivityForm
import uuid
import boto3
import os


## FUNCTION BASED VIEWS ##
def home(request):
  return render(request, "home.html")

def about(request):
  return render(request, "about.html")

@login_required
def trips_index(request):
  trips = Trip.objects.filter(user=request.user)
  return render(request, "trips/index.html", { "trips": trips })

@login_required
def trips_detail(request, trip_id):
  if request.user == Trip.objects.get(id=trip_id).user:
    trip = Trip.objects.get(id=trip_id)
    itinerary_form = ItineraryForm()
    return render(request, "trips/details.html", {"trip": trip, "itinerary_form": itinerary_form})
  else:
    raise PermissionDenied

@login_required
def itineraries_detail(request, itinerary_id):
  if request.user == Itinerary.objects.get(id=itinerary_id).trip.user:
    itinerary = Itinerary.objects.get(id=itinerary_id)
    activity_form = ActivityForm()
    return render(request, "itineraries/details.html", {"itinerary": itinerary, "activity_form": activity_form})
  else:
    raise PermissionDenied

## CLASS BASED VIEWS ##
 # trip views #
class TripCreate(LoginRequiredMixin, CreateView):
  model = Trip
  fields = ["trip_name", "locations", "start_date", "end_date"]
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user
    return super().form_valid(form)

class TripUpdate(LoginRequiredMixin, UpdateView):
  model = Trip
  fields = ["trip_name", "locations", "start_date", "end_date"]

class TripDelete(LoginRequiredMixin, DeleteView):
  model = Trip
  success_url = "/trips/"

 # itinerary views #
class ItineraryCreate(LoginRequiredMixin, CreateView):
  model = Itinerary
  fields = "__all__"
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user
    return super().form_valid(form)

class ItineraryUpdate(LoginRequiredMixin, UpdateView):
  model = Itinerary
  fields = ["date", "notes"]

  def get_success_url(self):
    itinerary_pk = self.object.id
    itinerary = Itinerary.objects.get(id=itinerary_pk)
    trip_detail_path = itinerary.trip.get_absolute_url()
    return trip_detail_path 

class ItineraryDelete(LoginRequiredMixin, DeleteView):
  model = Itinerary
  def get_success_url(self):
    itinerary_pk = self.object.id
    itinerary = Itinerary.objects.get(id=itinerary_pk)
    trip_detail_path = itinerary.trip.get_absolute_url()
    return trip_detail_path 

class ActivityDetail(DetailView):
  model = Activity

class ActivityCreate(LoginRequiredMixin, CreateView):
  model = Activity
  fields = "__all__"
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user
    return super().form_valid(form)

class ActivityUpdate(LoginRequiredMixin, UpdateView):
  model = Activity
  fields = "__all__"
  
  def get_success_url(self):
    activity_pk = self.object.id
    activity = Activity.objects.get(id=activity_pk)
    itinerary_detail_path = activity.itinerary.get_absolute_url()
    return itinerary_detail_path 

class ActivityDelete(LoginRequiredMixin, DeleteView):
  model = Activity
  
  def get_success_url(self):
    activity_pk = self.object.id
    activity = Activity.objects.get(id=activity_pk)
    itinerary_detail_path = activity.itinerary.get_absolute_url()
    return itinerary_detail_path 

 # form views #
@login_required
def add_itinerary(request, trip_id):
  #creating an itinerary form instance with a post request
  #passing data from our detail form 
  form = ItineraryForm(request.POST)
  if form.is_valid():
      #form.save will return a new instance of the itinerary
      #commit=False prevents it from being saved in the database, it remains in memory
      new_itinerary = form.save(commit=False)
      new_itinerary.trip_id = trip_id
      new_itinerary.save()
  return redirect("detail", trip_id=trip_id)

@login_required
def add_activity(request, itinerary_id):
  #creating an itinerary form instance with a post request
  #passing data from our detail form 
  form = ActivityForm(request.POST)
  if form.is_valid():
      new_activity = form.save(commit=False)
      new_activity.itinerary_id = itinerary_id
      new_activity.save()
  return redirect("itineraries_detail", itinerary_id=itinerary_id)

@login_required
def add_photo(request, activity_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get("photo-file", None)
    if photo_file:
        s3 = boto3.client("s3")
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind("."):]
        # just in case something goes wrong
        try:
            bucket = os.environ["S3_BUCKET"]
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, activity_id=activity_id)
        except Exception as e:
            print("An error occurred uploading file to S3")
            print(e)
    return redirect("activities_detail", pk=activity_id)

def signup(request):
  error_message = ""
  if request.method == "POST":
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect("about")
    else:
      error_message = "Invalid sign up - try again"
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {"form": form, "error_message": error_message}
  return render(request, "registration/signup.html", context)
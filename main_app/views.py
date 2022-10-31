from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Trip, Itinerary, Activity
from .forms import ItineraryForm

# Create your views here.
# Define the home view
def home(request):
  return render(request, "home.html")

def about(request):
  return render(request, 'about.html')

def trips_index(request):
    trips = Trip.objects.all()
    return render(request, "trips/index.html", { 'trips': trips })

def trips_detail(request, trip_id):
  trip = Trip.objects.get(id=trip_id)
  return render(request, "trips/details.html", {"trip": trip})

class TripCreate(CreateView):
    model = Trip
    fields = "__all__" 

class TripUpdate(UpdateView):
  model = Trip
  #disallow changing location? otherwise delete and start new trip
  fields = ["trip_name", "start_date", "end_date"]

class TripDelete(DeleteView):
  model = Trip
  success_url = "/trips/"

class ItineraryList(ListView):
  model = Itinerary

class ItineraryDetail(DetailView):
  model = Itinerary

class ItineraryCreate(CreateView):
  model = Itinerary
  fields = "__all__"

class ItineraryUpdate(UpdateView):
  model = Itinerary
  fields = "__all__"

class ItineraryDelete(DeleteView):
  model = Itinerary
  success_url = '/itineraries/'

class ActivityList(ListView):
  model = Activity

class ActivityDetail(DetailView):
  model = Activity

class ActivityCreate(CreateView):
  model = Activity
  fields = "__all__"

class ActivityUpdate(UpdateView):
  model = Activity
  fields = "__all__"

class ActivityDelete(DeleteView):
  model = Itinerary
  success_url = '/activities/'

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


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('about')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
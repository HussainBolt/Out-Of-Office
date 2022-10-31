from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path("trips/", views.trips_index, name="index"),
    path("trips/<int:trip_id>/", views.trips_detail, name="detail"),
    path('trips/create/', views.TripCreate.as_view(), name="trips_create"),
    path("trips/<int:pk>/update/", views.TripUpdate.as_view(), name="trips_update"),
    path("trips/<int:pk>/delete/", views.TripDelete.as_view(), name="trips_delete"),
    path('accounts/signup/', views.signup, name='signup'),

    #URL FOR Itinerary
    #NOTe :comment it out so it does not affect your code

    #Path for adding an itinerary to particular trip
    path("trips/<int:trip_id>/add_itinerary/", views.add_itinerary, name="add_itinerary"),

    # Path for itinerary after it has been added to trips
    path("itineraries/", views.ItineraryList.as_view(), name="itineraries_index"),
    path("itineraries/<int:pk>/", views.ItineraryDetail.as_view(), name="itineraries_detail"), 
    path("itineraries/create/", views.ItineraryCreate.as_view(), name="itineraries_create"),
    path("itineraries/<int:pk>/update/", views.ItineraryUpdate.as_view(), name="itineraries_update"),
    path("itineraries/<int:pk>/delete/", views.ItineraryDelete.as_view(), name="itineraries_delete"),

    #URL FOR time slots
    #NOTe :comment it out so it does not affect your code
    path("activities/", views.ActivityList.as_view(), name="activities_index"),
    path("activities/<int:pk>/", views.ActivityDetail.as_view(), name="activities_detail"), 
    path("activities/create/", views.ActivityCreate.as_view(), name="activities_create"),
    path("activities/<int:pk>/update/", views.ActivityUpdate.as_view(), name="activities_update"),
    path("activities/<int:pk>/delete/", views.ActivityDelete.as_view(), name="activities_delete"),

]
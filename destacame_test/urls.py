"""destacame_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from buses import views as buses_views
from places import views as places_views
from routes import views as routes_views
from schedules import views as schedules_views
from seats import views as seats_views
from drivers import views as drivers_views
from accounts import views as accounts_views

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts URLs
    path('accounts/new/', accounts_views.accounts_register_view),
    path('accounts/login/', obtain_auth_token, name="login"),

    # Places URLs
    path('places/', places_views.places_list_view),
    path('places/new/', places_views.places_new_place_view),
    path('places/<int:id>/', places_views.places_detail_place_view),


    # Schedules URLs
    path('schedules/', schedules_views.schedules_list_view),
    path('schedules/new/', schedules_views.schedules_new_schedule_view),
    path('schedules/<int:id>/', schedules_views.schedules_detail_schedule_view),
    path('schedules/<int:id>/available_seats',
         schedules_views.schedules_available_seats),

    # Routes URLs
    path('routes/', routes_views.routes_list_view),
    path('routes/new/', routes_views.routes_new_route_view),
    path('routes/<int:id>/', routes_views.routes_detail_route_view),
    path('routes/<int:id>/average_passengers',
         routes_views.routes_average_passengers_view),
    path('routes/<int:id>/bus_passengers_sold',
         routes_views.routes_bus_passengers_sold_view),

    # Buses URLs
    path('buses/', buses_views.buses_list_view),
    path('buses/new/', buses_views.buses_new_bus_view),
    path('buses/<int:id>/', buses_views.buses_detail_bus_view),

    # Drivers URLs
    path('drivers/', drivers_views.drivers_list_view),
    path('drivers/new/', drivers_views.drivers_new_driver_view),
    path('drivers/<int:id>/', drivers_views.drivers_detail_driver_view),

    # Seats URLs
    path('seats/', seats_views.seats_list_view),
    path('seats/new/', seats_views.seats_new_seat_view),
    path('seats/<int:id>/', seats_views.seats_detail_seat_view),

]

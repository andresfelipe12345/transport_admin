from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Route
from places.models import Place
from buses.models import Bus
from buses.serializers import BusSerializer
from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer
from seats.models import Seat
from .serializers import RouteSerializer
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime


class RouteView(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


@api_view(['GET'])
def routes_list_view(request):
    """
    List all routes.
    """
    if request.method == "GET":
        routes = Route.objects.all()
        serializer = RouteSerializer(
            routes, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


@api_view(['POST'])
def routes_new_route_view(request):
    """
    Create a new route
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            if data["place_origin"] == data["place_destination"]:
                raise Exception(
                    "Place origin and place destination must be different")
            place_origin = Place.objects.get(id=data["place_origin"])
            place_destination = Place.objects.get(id=data["place_destination"])
            new_route = Route.objects.create(
                place_origin=place_origin, place_destination=place_destination)
            success_message = {
                "success": "Route created"
            }
            return JsonResponse(success_message, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = {
                "Error": "Invalid request, " + str(e)
            }
            return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def routes_average_passengers_view(request, id):
    """
    Retrieve, the average number of passengers given a route, in a
    range of dates, the dates are URL parameters
    """
    # Convert the input dates to correct time zones
    date_to = request.GET.get("date_to") + " 23:59:59"
    date_to = timezone.make_aware(parse_datetime(
        date_to), timezone.get_current_timezone())
    date_from = request.GET.get("date_from") + " 00:00:00"
    date_from = timezone.make_aware(parse_datetime(
        date_from), timezone.get_current_timezone())
    # Get all the schedules for the route and range of dates
    schedules = Schedule.objects.filter(route=id,
                                        schedule_time__range=[date_from, date_to])
    seats_per_schedule = 0
    # Get all the seats sold for each schedule
    for schedule in schedules:
        seats = Seat.objects.filter(schedule=schedule.id)
        seats_per_schedule = seats_per_schedule + seats.count()
    # Calculate the average, capturing possible zero division error
    try:
        seats_per_schedule = seats_per_schedule / schedules.count()
    except Exception as e:
        error_message = {
            "message": "No average for that particular route"
        }
        return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)
    success_message = {
        "average": seats_per_schedule
    }
    return JsonResponse(success_message, status=status.HTTP_200_OK, safe=False)


@api_view(['GET'])
def routes_bus_passengers_sold_view(request, id):
    """
    Filter all the buses from a particular route with
    more than X percentage of its capacity sold.
    parameter id its the id of the route
    and url parameters for the percentage
    """
    # Get all the schedules for the route
    schedules = Schedule.objects.filter(route=id)
    percentage_minimum = 0
    try:
        # Get the percentage from the url parameters, in case
        # no percentage parameter sent, the value will be 0
        percentage_minimum = int(request.GET.get("percentage"))
    except Exception as e:
        error_message = {
            "Error": "Invalid request, " + str(e)
        }
        return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)
    buses = []
    # Go through the schedules
    for schedule in schedules:
        # Get the property max capaticy from the bus for each
        # particular schedule
        bus = Bus.objects.get(id=schedule.bus.id)
        max_capacity_bus = bus.seats
        # Get the seats sold on for the schedule
        seats = Seat.objects.filter(schedule=schedule.id)
        # Calculate the percentage
        percentage_calculated = (seats.count() * 100) / max_capacity_bus
        if percentage_calculated >= percentage_minimum:
            dict = {"schedule": ScheduleSerializer(
                schedule).data, "percentage_sold_on_bus": percentage_calculated, "seats_sold": seats.count()}
            buses.append(dict)
    return JsonResponse(buses, status=status.HTTP_200_OK, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
def routes_detail_route_view(request, id):
    """
    Retrieve, update or delete a route.
    """
    try:
        route = Route.objects.get(id=id)
    except Route.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RouteSerializer(route)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            if request.data["place_origin"] == request.data["place_destination"]:
                raise Exception(
                    "Place origin and place destination must be different")
            serializer = RouteSerializer(route, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = {
                "Error": "Invalid request, " + str(e)
            }
            return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        route.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

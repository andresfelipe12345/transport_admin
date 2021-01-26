from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Schedule
from routes.models import Route
from buses.models import Bus
from seats.models import Seat
from .serializers import ScheduleSerializer
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime


@api_view(['GET'])
def schedules_list_view(request):
    """
    List all routes.
    """
    if request.method == "GET":
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(
            schedules, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def schedules_available_seats(request, id):
    """
    List all the seats available for a particular schedule.
    """
    if request.method == "GET":
        try:
            schedule = Schedule.objects.get(id=id)
        except Schedule.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        bus = schedule.bus
        bus_seats = int(bus.seats)
        seats = Seat.objects.filter(schedule=id).order_by("seat_number")
        available_seats = []
        for seat_position_pivot in range(1, bus_seats+1):
            available_seats.append(seat_position_pivot)
        for seat in seats:
            available_seats.remove(seat.seat_number)
        return JsonResponse(available_seats, safe=False)


@api_view(['POST'])
def schedules_new_schedule_view(request):
    """
    Create a new schedule
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            route = Route.objects.get(id=data["route"])
            bus = Bus.objects.get(id=data["bus"])
            new_schedule = Schedule.objects.create(
                route=route, bus=bus, schedule_time=timezone.make_aware(parse_datetime(
                    data["schedule_time"]), timezone.get_current_timezone()))
            success_message = {
                "success": "Schedule created"
            }
            return JsonResponse(success_message, status=201)
        except Exception as e:
            error_message = {
                "Error": "Invalid request, " + str(e)
            }
            return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def schedules_detail_schedule_view(request, id):
    """
    Retrieve, update or delete a schedule.
    """
    try:
        item = Schedule.objects.get(id=id) or None
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ScheduleSerializer(item)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ScheduleSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

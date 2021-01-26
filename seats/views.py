from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Seat
from schedules.models import Schedule
from .serializers import SeatSerializer
from django.http import HttpResponse, JsonResponse


@api_view(['GET'])
def seats_list_view(request):
    """
    List all routes.
    """
    if request.method == "GET":
        seats = Seat.objects.all()
        serializer = SeatSerializer(
            seats, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def seats_new_seat_view(request):
    """
    Create a new schedule
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            schedule = Schedule.objects.get(id=data["schedule"])
            bus = schedule.bus
            bus_seats = int(bus.seats)
            if bus_seats < int(data["seat_number"]):
                raise Exception("The seat number is invalid")
            new_seat = Seat.objects.create(
                schedule=schedule, seat_number=int(data["seat_number"]), passenger_name=data["passenger_name"], passenger_email=data["passenger_email"])
            success_message = {
                "success": "Schedule created"
            }
        except Exception as e:
            error_message = {
                "Error": "Invalid request, " + str(e)
            }
            return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)
        success_message = SeatSerializer(new_seat)
        return Response(success_message.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def seats_detail_seat_view(request, id):
    """
    Retrieve, update or delete a route.
    """
    try:
        seat = Seat.objects.get(id=id)
    except Seat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SeatSerializer(seat)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SeatSerializer(seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

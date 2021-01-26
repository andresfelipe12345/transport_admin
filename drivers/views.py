from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Driver
from buses.models import Bus
from .serializers import DriverSerializer
from django.http import HttpResponse, JsonResponse


@api_view(['GET'])
def drivers_list_view(request):
    """
    List all drivers.
    """
    if request.method == "GET":
        drivers = Driver.objects.all()
        serializer = DriverSerializer(
            drivers, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def drivers_new_driver_view(request):
    """
    Create a new driver
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        bus = None
        if "bus" in data:
            try:
                bus = Bus.objects.get(id=data["bus"])
            except:
                error_message = {
                    "Error": "Bus ID was invalid"
                }
                return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_driver = Driver.objects.create(
                name=data["name"], bus=bus)
            success_message = {
                "success": "Route created"
            }
            return JsonResponse(success_message, status=201)
        except:
            error_message = {
                "Error": "The input data is invalid"
            }
            return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def drivers_detail_driver_view(request, id):
    """
    Retrieve, update or delete a driver.
    """
    try:
        driver = Driver.objects.get(id=id)
    except Driver.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DriverSerializer(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

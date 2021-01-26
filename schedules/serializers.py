from rest_framework import serializers
from routes.serializers import RouteSerializer
from buses.serializers import BusSerializer

from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = ["id", "schedule_time", "route", "bus"]
        depth = 2

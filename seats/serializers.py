from rest_framework import serializers

from .models import Seat


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = ["id", "seat_number", "seat_code",
                  "passenger_name", "passenger_email", "schedule"]
        depth = 3

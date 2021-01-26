from rest_framework import serializers
from places.serializers import PlaceSerializer

from .models import Route


class RouteSerializer(serializers.ModelSerializer):

    place_origin = PlaceSerializer(many=False, read_only=True)
    place_destination = PlaceSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = ["id", "place_origin", "place_destination"]

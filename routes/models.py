from django.db import models
from places.models import Place


class Route(models.Model):
    place_origin = models.ForeignKey(
        Place, null=False, on_delete=models.DO_NOTHING, related_name="origin")
    place_destination = models.ForeignKey(
        Place, null=False, on_delete=models.DO_NOTHING, related_name="destination")

    class Meta:
        unique_together = ("place_origin", "place_destination")

    def __str__(self):
        return "route: " + self.place_origin.name + " to " + self.place_destination.name

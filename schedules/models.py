from django.db import models
from routes.models import Route
from buses.models import Bus


class Schedule(models.Model):
    route = models.ForeignKey(
        Route, null=False, on_delete=models.CASCADE)
    bus = models.ForeignKey(
        Bus, null=True, on_delete=models.SET_NULL)
    schedule_time = models.DateTimeField(null=False)

    class Meta:
        unique_together = ("route", "bus", "schedule_time")

    def __str__(self):
        routes = str(self.route.place_origin.name) + " - " + \
            str(self.route.place_destination.name)
        return "schedule: " + str(self.bus.id) + " - " + str(self.schedule_time) + " - " + routes

from django.db import models


class Bus(models.Model):
    seats = models.IntegerField(default=10, null=True, blank=True)
    operative = models.BooleanField(default=True, null=False)

    def __str__(self):
        return "bus: " + str(self.id)

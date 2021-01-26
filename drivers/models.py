from django.db import models
from buses.models import Bus


class Driver(models.Model):
    name = models.CharField(max_length=50, null=False)
    bus = models.OneToOneField(Bus, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

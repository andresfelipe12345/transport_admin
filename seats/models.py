from django.db import models
from schedules.models import Schedule
import random
import string


class Seat(models.Model):
    schedule = models.ForeignKey(
        Schedule, null=False, on_delete=models.CASCADE)
    seat_number = models.IntegerField(null=False)

    seat_code = models.CharField(
        max_length=6, null=True, unique=True)
    passenger_name = models.CharField(max_length=50, null=False)
    passenger_email = models.EmailField(max_length=254, null=False)

    class Meta:
        unique_together = ("schedule", "seat_number")

    def id_generator(self):
        size = 6
        chars = string.ascii_uppercase + string.digits
        print("en el id")
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        if not self.seat_code:
            # Generate ID once, then check the db. If exists, keep trying.
            size = 6
            chars = string.ascii_uppercase + string.digits
            self.seat_code = ''.join(random.choice(chars) for _ in range(size))
            while Seat.objects.filter(seat_code=self.seat_code).exists():
                self.urlhaseat_codesh = id_generator()
        super(Seat, self).save()

    def __str__(self):
        return "Seat : " + str(self.seat_number) + " - " + self.seat_code

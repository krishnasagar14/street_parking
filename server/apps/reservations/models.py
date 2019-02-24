from django.db import models
from django.conf import settings

from common.models import baseModel
from apps.parkSpot.models import parkingSpot
# Create your models here.

class Reservations(baseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spot = models.ForeignKey('parkSpot.parkingSpot', on_delete=models.DO_NOTHING)
    duration = models.IntegerField('time peroid of reservation in hours')
from django.db import models

from common.models import baseModel

# Create your models here.

class parkingSpot(baseModel):
    lat = models.IntegerField('latitude of spot', db_index=True, blank=False)
    longi = models.IntegerField('longitude of spot', db_index=True, blank=False)
    spot_addr = models.TextField('spot address', blank=True)
    cost_per_hr = models.PositiveIntegerField('cost of spot for parking', blank=False)
    is_reserved = models.BooleanField('is spot reserved or not', default=False)

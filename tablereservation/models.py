from django.db import models

# Create your models here.
from table.models import Table


class Reservation(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='table_reservation')
    date = models.DateField()

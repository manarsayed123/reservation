from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Table(models.Model):
    number = models.IntegerField(unique=True)
    num_of_seats = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])

    def __str__(self):
        return self.number

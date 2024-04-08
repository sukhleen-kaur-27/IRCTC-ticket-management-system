from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username


class Train(models.Model):
    train_number=models.CharField(max_length=10, unique=True)
    departureCity = models.CharField(max_length=10)
    arrivalCity = models.CharField(max_length=20)
    dateOfDeparture = models.DateField()
    timeOfDeparture = models.TimeField()
    timeOfArrival = models.TimeField()
    numberOfSeats = models.IntegerField()

    def __str__(self):
        return self.train_number
    
class Reservation(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    passenger = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
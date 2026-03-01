from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class Room(models.Model):
    ROOM_TYPES = [
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe Room'),
        ('standard', 'Standard Room')
    ]

    CURRENCY_TYPES = [
        ('USD', 'US Dollar'),
        ('NPR', 'Nepalese Rupee')
    ]

    name = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(max_length=100, choices=ROOM_TYPES)
    pricePerNight = models.IntegerField(default=150)
    currency = models.CharField(default='NPR', max_length=10, choices=CURRENCY_TYPES)
    maxOccupancy = models.IntegerField(default=1)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name}  ({self.type})"
    
class RoomImage(models.Model):
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True)
    room = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.room.name} - {self.caption or 'No Caption'}"
    
class OccupiedDates(models.Model):
    room = models.ForeignKey(Room, related_name='occupieddates', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='booked_dates', on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.date} - {self.room.name} booked by {self.user.full_name}"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, default='')
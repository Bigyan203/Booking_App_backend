from django.db import models

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
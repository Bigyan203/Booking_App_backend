from rest_framework import serializers
from .models import Room,RoomImage,OccupiedDates,User
from django.contrib.auth.hashers import make_password

class RoomImageSerializer(serializers.ModelSerializer):
    room =serializers.HyperlinkedRelatedField(
        view_name='room-detail',
        queryset=Room.objects.all()),
    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'caption', 'room']

class OccupiedDatesSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        view_name='room-detail',
        queryset=Room.objects.all()
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    
    class Meta:
        model = OccupiedDates
        fields = ['url', 'id', 'room', 'date', 'user']
        extra_kwargs = {        #yo part afai rakeko, url recognize nagareko vera
            'url': {'view_name': 'occupied-dates-detail'}
        }

    def validate(self, data):
        """Check if the room is already booked for the given date"""
        room = data.get('room')
        date = data.get('date')
        
        # If updating an existing booking, exclude the current instance
        if self.instance:
            if OccupiedDates.objects.filter(room=room, date=date).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError(
                    "This room is already booked for the selected date."
                )
        else:
            # For new bookings
            if OccupiedDates.objects.filter(room=room, date=date).exists():
                raise serializers.ValidationError(
                    "This room is already booked for the selected date."
                )
        
        return data

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    occupied_dates = OccupiedDatesSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['url', 'id', 'name', 'type', 'pricePerNight', 'currency', 'maxOccupancy', 'description', 'images', 'occupied_dates']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username' , 'email', 'full_name', 'password']
        extra_kwargs = {
            'url': {'view_name': 'user-detail'}
        }

    def validate_password(self, value):
        return make_password(value)
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

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ['url', 'id', 'name', 'type', 'pricePerNight', 'currency', 'maxOccupancy', 'description', 'images']

class OccupiedDatesSerializer(serializers.HyperlinkedModelSerializer):
    room = serializers.HyperlinkedRelatedField(
        view_name='room-detail',
        queryset=Room.objects.all()
    )

    class Meta:
        model = OccupiedDates
        fields = ['url', 'id', 'room', 'date']
        extra_kwargs = {        #yo part afai rakeko, url recognize nagareko vera
            'url': {'view_name': 'occupied-dates-detail'}
        }

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
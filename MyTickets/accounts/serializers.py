from rest_framework import serializers
from .models import *
from django.forms.models import model_to_dict

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model=Train
        fields = '__all__'
    
class TrainAvailableSerializer(serializers.ModelSerializer):
    seats_Available = serializers.SerializerMethodField("numOfSeats")
    class Meta:
        model=Train
        fields = '__all__'
    def numOfSeats(self, obj):
        request = self.context.get('request')
        reservation = Reservation.objects.filter(train=request.data["train_number"])
        return (obj.numberOfSeats - len(reservation))

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reservation
        fields = '__all__'

class DetailsSerializer(serializers.ModelSerializer):
    train_details = serializers.SerializerMethodField("train_details_method")
    passenger_details = serializers.SerializerMethodField("passenger_details_method")
    class Meta:
        model = Reservation
        fields = '__all__'
    
    def train_details_method(self, obj):
        request = self.context.get('request')
        train_details__ = Train.objects.filter(train_number = request.data['train_number'])
        if len(train_details__)==0:
            return {}
        else:
            return model_to_dict(train_details__[0])

    
    def passenger_details_method(self, obj):
        request = self.context.get('request')
        passenger_details__ = CustomUser.objects.filter(email = request.data['email'])
        if len(passenger_details__)==0:
            return {}
        else: 
            return model_to_dict(passenger_details__[0])
  
    

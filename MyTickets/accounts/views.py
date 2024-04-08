from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from django.forms.models import model_to_dict

from .serializers import *
from .models import *

# Create your views here.

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def user_login(request):
    if request.method=='POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try : 
                user=CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass
        
        if not user:
            user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error':"Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method=='POST':
        try:
            request.user.auth_token.delete()
            return Response({'message':"Succeccfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_seat_availablility(request):
    if request.method == 'POST':
        trains = Train.objects.filter(departureCity = request.data["departureCity"], arrivalCity = request.data["arrivalCity"], dateOfDeparture = request.data["dateOfDeparture"])
        if len(trains)==0:
            return Response({"message":"No trains between this Route."}, status=status.HTTP_200_OK)
        # paginator = PageNumberPagination()
        # paginator.page_size = 1
        # result_page = paginator.paginate_queryset(trains, request)
        # serializer = TrainAvailableSerializer(data = model_to_dict(trains), many=True, context= {"request":request})
        # if serializer.is_valid():
        #     serializer.save()
        else:
            all_details = {}
            for train in trains:
                train_details = TrainSerializer(model_to_dict(train)).data
                all_details[train.train_number] = train_details
            return Response(all_details, status=status.HTTP_200_OK)
    return Response({}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([HasAPIKey])
def add_train(request):
    if request.method == "POST":
        train_number = request.data['train_number']
        departureCity = request.data['departureCity']
        arrivalCity = request.data['arrivalCity']
        dateOfDeparture = request.data['dateOfDeparture']
        timeOfDeparture = request.data['timeOfDeparture']
        timeOfArrival = request.data['timeOfArrival']
        numberOfSeats = request.data['numberOfSeats']
        # train = Train(train_number = train_number,departureCity =  departureCity, arrivalCity = arrivalCity, dateOfDeparture = dateOfDeparture, timeOfDeparture = timeOfDeparture,  timeOfArrival = timeOfArrival, numberOfSeats = numberOfSeats)
        # train.save()
        serializer = TrainSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def train_reservation(request):
    if request.method=='POST':
        train = Train.objects.filter(train_number = request.data['train_number'])
        if len(train)==0:
            return Response({"Error":"No Train by this Number"}, status=status.HTTP_204_NO_CONTENT)
        user = CustomUser.objects.filter(email = request.data['email'])
        if len(user)==0:
            return Response({"Error":"No user by this email"}, status=status.HTTP_204_NO_CONTENT)
        numReserved = Reservation.objects.filter(train__train_number = train[0].train_number)
        if len(numReserved) == train[0].numberOfSeats:
            return Response({"Error": "No Seats Avaiable"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # reservation_obj = Reservation(train = train[0], passenger = user[0])
        serializer = ReservationSerializer(data={"train":train[0].pk, "passenger":user[0].pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_details(request):
    if request.method=='POST':
        details = Reservation.objects.filter(train__train_number = request.data['train_number'], passenger__email = request.data['email'])
        if len(details)==0:
            return Response({}, status=status.HTTP_200_OK)
        details_serializer = DetailsSerializer(details[0], context = {"request":request})
        return Response(details_serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"Error":"Something went wrong"}, status=status.HTTP_502_BAD_GATEWAY)
    
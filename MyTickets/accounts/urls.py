from django.urls import path
from .views import *
urlpatterns = [
    path('register/', register_user, name='register'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('add_train/', add_train, name='add_train'),
    path('get_seat/', get_seat_availablility, name='get_seat'),
    path('reserve_seat/', train_reservation, name='reserve_seat'),
    path('get_details/', get_details, name='get_details'),
    

]
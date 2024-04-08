from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Train)
admin.site.register(CustomUser)

@admin.register(Reservation)
class ReservationModelAdmin(admin.ModelAdmin):
    search_fields = ('train__train_number',)
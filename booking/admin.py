from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TravelOption, Booking

admin.site.register(TravelOption)
admin.site.register(Booking)
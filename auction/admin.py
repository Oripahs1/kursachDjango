from django.contrib import admin
from .models import Car, CarForPage, PhotoCar

admin.site.register(Car)
admin.site.register(PhotoCar)
admin.site.register(CarForPage)
# Register your models here.

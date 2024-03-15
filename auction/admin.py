from django.contrib import admin
from .models import Car, CarForPage, PhotoCar, Worker

admin.site.register(Car)
admin.site.register(PhotoCar)
admin.site.register(CarForPage)
admin.site.register(Worker)
# Register your models here.

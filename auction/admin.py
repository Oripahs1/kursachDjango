from django.contrib import admin
from .models import Car, PhotoCar, Worker, Invoice

admin.site.register(Car)
admin.site.register(PhotoCar)
admin.site.register(Worker)
admin.site.register(Invoice)
# Register your models here.

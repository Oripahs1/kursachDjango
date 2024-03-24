from django.contrib import admin
from .models import Car, PhotoCar, Worker, Order, Customer
from .models import Car, PhotoCar, Worker, Invoice

admin.site.register(Car)
admin.site.register(PhotoCar)
admin.site.register(Worker)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(Customer)
# Register your models here.

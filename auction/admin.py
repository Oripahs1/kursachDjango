from django.contrib import admin
from .models import Car, PhotoCar, Worker, Invoice, Order, Customer
from django.contrib.auth.admin import UserAdmin

admin.site.register(Worker, UserAdmin)

admin.site.register(Car)
admin.site.register(PhotoCar)
# admin.site.register(Worker)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(Customer)
# Register your models here.

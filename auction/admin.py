from django.contrib import admin
from django import forms
from .models import Car, PhotoCar, Worker, Invoice, Order, Customer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

admin.site.register(Car)
admin.site.register(PhotoCar)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(Customer)

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Worker
        fields = ('username', 'password', 'full_name', 'job_title', 'phone_number', 'passport')

    def passport_clean(self):
        passport = self.cleaned_data['passport']
        if Worker.objects.filter(passport=passport).exists():
            return None
        return passport

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('username', 'full_name', 'job_title', 'phone_number', 'passport')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username', 'full_name', 'job_title', 'phone_number', 'passport', 'is_superuser', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone_number', 'passport')}),
        ('Job_title', {'fields': ('job_title',)}),
    )


admin.site.register(Worker, UserAdmin)

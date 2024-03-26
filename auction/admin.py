from django.contrib import admin
from django import forms
from .models import Car, PhotoCar, Worker, Invoice, Order, Customer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

admin.site.register(Car)
admin.site.register(PhotoCar)
# admin.site.register(Worker)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(Customer)


# Register your models here.


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150,
    #                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    # full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # job_title = forms.ChoiceField(label='Должность', choices=Worker.JOB_CHOICE,
    #                               widget=forms.Select(attrs={'class': 'custom-select'}))
    # passport = forms.CharField(label='Серия и номер паспорта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # phone_num = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    # password1.widget.attrs.update({'class': 'form-control'})
    # password2.widget.attrs.update({'class': 'form-control'})

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Worker
        fields = ('username', 'password', 'full_name', 'job_title', 'phone_number', 'passport')

    # def username_clean(self):
    #     username = self.cleaned_data['username']
    #     if Worker.objects.filter(username=username).exists():
    #         return None
    #     return username

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
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    class Meta:
        model = Worker
        fields = ('username', 'full_name', 'job_title', 'phone_number', 'passport')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('username', 'full_name', 'job_title', 'phone_number', 'passport', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone_number', 'passport')}),
        ('Job_title', {'fields': ('job_title',)}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'date_of_birth', 'password1', 'password2'),
    #     }),
    # )
    # search_fields = ('email',)
    # ordering = ('email',)
    # filter_horizontal = ()


admin.site.register(Worker, UserAdmin)

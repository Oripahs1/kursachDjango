from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.contrib import messages
from .models import Worker


class ParserForm(forms.Form):
    url_parser_field = forms.CharField(label='Cars url')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(min_length=3, max_length=65, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):

    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150)
    job_title = forms.ChoiceField(label='Должность', choices=Worker.JOB_CHOICE)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    def username_clean(self):
        username = self.cleaned_data['username']
        new = Worker.objects.filter(full_name=username)
        if Worker.objects.filter(full_name=username).exists():
            return '#'
        return username

    # def email_clean(self):
    #     email = self.cleaned_data['email'].lower()
    #     new = User.objects.filter(email=email)
    #     if new.count():
    #         raise ValidationError(" Email Already Exist")
    #     return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2 or password1 == '' or password2 == '':
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        Worker.objects.create(
            full_name=self.cleaned_data['username'].strip(),
            job_title=self.cleaned_data['job_title'],
            password=self.cleaned_data['password1']
        )

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


class LogoutForm(forms.Form):
    url_parser_field = forms.CharField(label='Cars url')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(min_length=3, max_length=65, widget=forms.PasswordInput)

    def login_clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if Worker.objects.filter(username=username, password=password).exists():
            return username
        else:
            return '#'


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_title = forms.ChoiceField(label='Должность', choices=Worker.JOB_CHOICE, widget=forms.Select(attrs={'class': 'custom-select'}))
    passport = forms.CharField(label='Серия и номер паспорта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_num = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    password1.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'class': 'form-control'})

    def username_clean(self):
        username = self.cleaned_data['username']
        new = Worker.objects.filter(username=username)
        if Worker.objects.filter(username=username).exists():
            return '#'
        return username

    def passport_clean(self):
        passport = self.cleaned_data['passport']
        new = Worker.objects.filter(passport=passport)
        if Worker.objects.filter(passport=passport).exists():
            return '#'
        return passport

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
            username=self.cleaned_data['username'].strip(),
            full_name=self.cleaned_data['full_name'],
            job_title=self.cleaned_data['job_title'],
            passport=self.cleaned_data['passport'],
            phone_number=self.cleaned_data['phone_num'],
            password=self.cleaned_data['password1'],
        )
    def update(self, commit=True):
        worker_obl = Worker.objects.filter(username=self.cleaned_data['username'])
        print(worker_obl)
        worker_obl.update(
            username=self.cleaned_data['username'].strip(),
            full_name=self.cleaned_data['full_name'],
            job_title=self.cleaned_data['job_title'],
            passport=self.cleaned_data['passport'],
            phone_number=self.cleaned_data['phone_num'],
            password=self.cleaned_data['password1'],
        )


class UpdateWorker(forms.Form):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150, )
    full_name = forms.CharField(label='ФИО')
    job_title = forms.ChoiceField(label='Должность', choices=Worker.JOB_CHOICE)
    passport = forms.CharField(label='Серия и номер паспорта')
    phone_num = forms.CharField(label='Номер телефона')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class WorkerForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='ФИО')
    job_title = forms.ChoiceField(label='Должность', choices=Worker.JOB_CHOICE)
    passport = forms.CharField(label='Серия и номер паспорта')
    phone_num = forms.CharField(label='Номер телефона')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    def input_for_form(self, obj):
        print('Вроде заносим')
        print(obj.username)
        # print(self.cleaned_data)
        print(self.cleaned_data['username'])
        self.username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'value': obj.username}))
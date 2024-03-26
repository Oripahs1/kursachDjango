from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.contrib import messages
from .models import Worker, Order, Customer, Car, Invoice
from django.db import IntegrityError
import datetime


class ParserForm(forms.Form):
    url_parser_field = forms.CharField(label='Cars url')


class LogoutForm(forms.Form):
    pass


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=3, max_length=65, widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'form-control'})

    def login_clean(self):
        # username = self.cleaned_data['username']
        # password = self.cleaned_data['password']
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        # if Worker.objects.filter(username=username, password=password).exists():
        if not Worker.objects.filter(username=username).exists():
            return '#'
        return username


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_title = forms.ChoiceField(label='Должность', choices=Worker.JOB_CHOICE,
                                  widget=forms.Select(attrs={'class': 'custom-select'}))
    passport = forms.CharField(label='Серия и номер паспорта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    # password1.widget.attrs.update({'class': 'form-control'})
    # password2.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Worker
        exclude = ['username', 'password', 'full_name', 'job_title', 'phone_number', 'passport']

        # def __init__(self):
        #     self.username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150,
        #                                widget=forms.TextInput(attrs={'class': 'form-control'}))
        #     self.phone_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def username_clean(self):
        username = self.cleaned_data['username']
        if Worker.objects.filter(username=username).exists():
            return None
        return username

    def passport_clean(self):
        passport = self.cleaned_data['passport']
        if Worker.objects.filter(passport=passport).exists():
            return None
        return passport

    def clean_password2(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            return None
        return password1

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.username = self.cleaned_data['username']
    #     user.set_password(self.cleaned_data['password'])
    #     if commit:
    #         try:
    #             user.save()
    #             # Создание объекта Worker и сохранение его в базе данных
    #             Worker.objects.create(
    #                 user=user.username,
    #                 full_name=self.cleaned_data['full_name'],
    #                 job_title=self.cleaned_data['job_title'],
    #                 phone_number=self.cleaned_data['phone_number'],
    #                 passport=self.cleaned_data['passport']
    #             )
    #         except:
    #             return None
    #         return user
    #     else:
    #         return None
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password'])
        if commit:
            try:
                user.save()
                # Создание объекта Worker и сохранение его в базе данных
                worker = Worker.objects.create(
                    user=user,
                    full_name=self.cleaned_data['full_name'],
                    job_title=self.cleaned_data['job_title'],
                    phone_number=self.cleaned_data['phone_number'],
                    passport=self.cleaned_data['passport']
                )
                return user  # Возвращаем объект пользователя
            except IntegrityError:
                # Если произошла ошибка, например, номер паспорта неуникален
                user.delete()  # Удаляем созданного пользователя
                raise  # Переопределяем ошибку
        else:
            return None

        # user.set_password(password)
        # user.save(using=self._db)
        # return user
        # user = super(RegistrationForm, self).save(commit=False)
        # user.set_password(self.cleaned_data.get("password1"))
        # if commit:
        #     user.save()
        # return user

        # Worker.objects.create(
        #     username=self.cleaned_data['username'].strip(),
        #     full_name=self.cleaned_data['full_name'],
        #     job_title=self.cleaned_data['job_title'],
        #     passport=self.cleaned_data['passport'],
        #     phone_number=self.cleaned_data['phone_num'],
        #     password=self.cleaned_data['password1'],
        # )

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


class OrderForm(forms.Form):
    first_name_client = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name_client = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    patronymic_client = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.DateInput(
        attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'data-slots': '_'}))
    place_of_birth = forms.CharField(label='Место рождения', widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_series = forms.CharField(label='Серия паспорта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_number = forms.CharField(label='Номер паспорта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_department_code = forms.CharField(label='Код подразделения',
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_department_name = forms.CharField(label='Паспорт выдан',
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    id_car = forms.CharField(label='Машина', widget=forms.TextInput(attrs={'class': 'form-control'}))
    worker = forms.ModelChoiceField(label='Сотрудник', queryset=Worker.objects,
                                    widget=forms.Select(attrs={'class': 'custom-select'}), empty_label=None)

    def save(self, commit=True):
        customer = Customer.objects.create(
            first_name_client=self.cleaned_data['first_name_client'],
            last_name_client=self.cleaned_data['last_name_client'],
            patronymic_client=self.cleaned_data['patronymic_client'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            place_of_birth=self.cleaned_data['place_of_birth'],
            passport_series=self.cleaned_data['passport_series'],
            passport_number=self.cleaned_data['passport_number'],
            passport_department_code=self.cleaned_data['passport_department_code'],
            passport_department_name=self.cleaned_data['passport_department_name'],
            telephone=self.cleaned_data['telephone']
        )

        car = Car.objects.get(pk=self.cleaned_data['id_car'])
        Order.objects.create(
            id_customer=customer,
            id_worker=self.cleaned_data['worker'],
            id_car=car,
            date_start=datetime.date.today(),
        )


class OrderInOrdersForm(forms.Form):
    id_order = forms.CharField(label='Заказ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name_client = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control form-readonly', 'readonly': 'True'}))
    last_name_client = forms.CharField(label='Фамилия', widget=forms.TextInput(
        attrs={'class': 'form-control form-readonly', 'readonly': 'True'}))
    patronymic_client = forms.CharField(label='Отчество', widget=forms.TextInput(
        attrs={'class': 'form-control form-readonly', 'readonly': 'True'}))
    telephone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_start = forms.DateField(label='Дата открытия заказа', widget=forms.DateInput(
        attrs={'class': 'form-control form-readonly', 'readonly': 'True'}))
    date_end = forms.CharField(label='Дата закрытия заказа', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'data-slots': '_'}))
    comment = forms.CharField(label='Комментарий к заказу', widget=forms.Textarea(attrs={'class': 'form-control'}))
    sbts = forms.FileField(label='Добавить СБТС', widget=forms.FileInput(attrs={'class': 'form-control'}))
    ptd = forms.FileField(label='Добавить ПТД', widget=forms.FileInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        order = Order.objects.filter(id_order=self.cleaned_data['id_order'])
        order.update(
            date_end=self.cleaned_data['date_end'],
            comment=self.cleaned_data['comment'],
        )
        customer = order[0].id_customer
        customer.telephone = self.cleaned_data['telephone']
        customer.save()


class InvoiceForm(forms.Form):
    id_invoice = forms.IntegerField(label='ID',
                                    widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    payer = forms.CharField(label='Плательщик', widget=forms.TextInput(attrs={'class': 'form-control'}))
    seller = forms.CharField(label='Получатель', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_form = forms.CharField(label='Дата формирования',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-YYYY'}))
    date_pay = forms.CharField(label='Дата оплаты',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-YYYY'}))
    sum = forms.IntegerField(label='Сумма', widget=forms.TextInput(attrs={'class': 'form-control'}))
    check_document = forms.CharField(label='Скан чека', widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label='Тип счета на оплату', choices=Invoice.type_choice,
                             widget=forms.Select(attrs={'class': 'custom-select'}))
    scan = forms.CharField(label='Скан счета на оплату', widget=forms.TextInput(attrs={'class': 'form-control'}))
    assigning = forms.CharField(label='Назначение', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def update(self, commit=True):
        invoice_obl = Invoice.objects.filter(id_invoice=self.cleaned_data['id_invoice'])
        print(invoice_obl)
        invoice_obl.update(
            payer=self.cleaned_data['payer'],
            seller=self.cleaned_data['seller'],
            date_form=self.cleaned_data['date_form'],
            date_pay=self.cleaned_data['date_pay'],
            sum=self.cleaned_data['sum'],
            type=self.cleaned_data['type'],
            check_document=self.cleaned_data['check_document'],
            scan=self.cleaned_data['scan'],
            assigning=self.cleaned_data['assigning'],
        )


class NewInvoiceForm(forms.Form):
    payer = forms.CharField(label='Плательщик', widget=forms.TextInput(attrs={'class': 'form-control'}))
    seller = forms.CharField(label='Получатель', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_form = forms.CharField(label='Дата формирования',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-YYYY'}))
    date_pay = forms.CharField(label='Дата оплаты',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DD-MM-YYYY'}))
    sum = forms.IntegerField(label='Сумма', widget=forms.TextInput(attrs={'class': 'form-control'}))
    check_document = forms.CharField(label='Скан чека', widget=forms.TextInput(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label='Тип счета на оплату', choices=Invoice.type_choice,
                             widget=forms.Select(attrs={'class': 'custom-select'}))
    scan = forms.CharField(label='Скан счета на оплату', widget=forms.TextInput(attrs={'class': 'form-control'}))
    assigning = forms.CharField(label='Назначение', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        print('Пытаемся сохранить')
        Invoice.objects.create(
            payer=self.cleaned_data['payer'].strip(),
            seller=self.cleaned_data['seller'].strip(),
            date_form=self.cleaned_data['date_form'],
            date_pay=self.cleaned_data['date_pay'],
            sum=self.cleaned_data['sum'],
            type=self.cleaned_data['type'],
            check_document=self.cleaned_data['check_document'],
            scan=self.cleaned_data['scan'],
            assigning=self.cleaned_data['assigning'],
        )

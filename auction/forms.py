from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from django.contrib import messages
from .models import Worker, Order, Customer, Car, Invoice
import datetime


class ParserForm(forms.Form):
    url_parser_field = forms.CharField(label='Cars url')


class LogoutForm(forms.Form):
    url_parser_field = forms.CharField(label='Cars url')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(min_length=3, max_length=65, widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'form-control'})

    def login_clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if Worker.objects.filter(username=username, password=password).exists():
            return username
        else:
            return '#'


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_title = forms.ChoiceField(label='Должность', choices=Worker.JOB_CHOICE,
                                  widget=forms.Select(attrs={'class': 'custom-select'}))
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


class TextareaWithValueHandling(forms.Textarea):
    """
    Ugly hack to get a default value preset within a textarea. (not supported by django)
    This template renders widget.attrs.value within the textarea body if there is no real value
    """
    template_name = 'form/widget/textarea_with_value_handling.html'


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
        attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'data-slots': '_'}), required=False)
    comment = forms.CharField(label='Комментарий к заказу', widget=forms.Textarea(attrs={'class': 'form-control'}),
                              required=False)
    sbts = forms.FileField(label='СБТС', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                           required=False)
    ptd = forms.FileField(label='ПТД', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)

    def save(self, commit=True):
        order = Order.objects.filter(id_order=self.cleaned_data['id_order'])
        if self.cleaned_data['date_end'] != '':
            order.update(date_end=self.cleaned_data['date_end'])

        order.update(
            comment=self.cleaned_data['comment']
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

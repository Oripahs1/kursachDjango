from django import forms
from .models import Worker, Order, Customer, Car, Invoice, Duty, Price, CustomsDuty, Excise, TransportCompany, \
    TransportCompanyPrice
from django.db import IntegrityError
import datetime


class ParserForm(forms.Form):
    url_parser_field = forms.CharField(label='Cars url')


class LogoutForm(forms.Form):
    pass


class LoginForm(forms.Form):
    username = forms.CharField(label = 'Имя пользователя', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label = 'Пароль', min_length=1, max_length=65, widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'form-control'})



class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_title = forms.ChoiceField(label='Должность', choices=Worker.JOB_CHOICE,
                                  widget=forms.Select(attrs={'class': 'custom-select'}))
    passport = forms.CharField(label='Серия и номер паспорта',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_active = forms.BooleanField(initial=True, widget=forms.HiddenInput())  # Установим is_active в True по умолчанию
    is_staff = forms.BooleanField(initial=True, widget=forms.HiddenInput())  # Установим is_staff в True по умолчанию

    class Meta:
        model = Worker
        exclude = ['username', 'password']

    def passport_clean(self):
        passport = self.cleaned_data.get('passport')
        if Worker.objects.filter(passport=passport).exists():
            return None
            # raise ValidationError("Пользователь с таким паспортом уже существует.")
        return passport

    def username_clean(self):
        username = self.cleaned_data.get('username')
        if Worker.objects.filter(username=username).exists():
            return None
            # raise ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            return None
            # raise ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.is_active = True  # Установим is_active в True
            user.is_staff = True  # Установим is_staff в True
            if user.pk is None:  # Если пользователь новый
                existing_user = Worker.objects.filter(username=user.username).exists()
                if existing_user:
                    raise IntegrityError("User with this username already exists.")
                user.save()

            # Если пользователь уже существует, обновляем его поля
            else:
                # Устанавливаем username для обновления
                user.username = self.cleaned_data['username']
                user.save()

            # Создаем объект Worker и сохраняем его в базе данных
            worker, created = Worker.objects.get_or_create(
                username=user.username,  # Сохраняем username при создании нового работника
                defaults={
                    'full_name': self.cleaned_data['full_name'],
                    'job_title': self.cleaned_data['job_title'],
                    'phone_number': self.cleaned_data['phone_number'],
                    'passport': self.cleaned_data['passport'],
                }
            )

            if not created:
                # Если работник уже существует, обновляем его остальные поля
                worker.full_name = self.cleaned_data['full_name']
                worker.job_title = self.cleaned_data['job_title']
                worker.phone_number = self.cleaned_data['phone_number']
                worker.passport = self.cleaned_data['passport']
                worker.save()

            return user  # Возвращаем объект пользователя
        else:
            return None

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
    customer = forms.ModelChoiceField(label='Клиент', queryset=Customer.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}), empty_label=None)
    delivery = forms.ChoiceField(label='Доставка', choices=Order.NEEDS_DELIVERY,
                             widget=forms.Select(attrs={'class': 'custom-select'}))
    city = forms.ChoiceField(
        label='Доставка',
        choices=[(place, f"{place} - {price} руб.") for place, price in
                 TransportCompanyPrice.objects.values_list('place', 'price').distinct()],
        widget=forms.Select(attrs={'class': 'custom-select'})
    )
    id_car = forms.CharField(label='Машина', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # worker = forms.ModelChoiceField(label='Сотрудник',
    #                                 queryset=Worker.objects.filter(is_superuser=False, job_title='Менеджер'),
    #                                 widget=forms.Select(attrs={'class': 'custom-select'}), empty_label=None)
    worker = forms.CharField(label='Сотрудник',
                             widget=forms.TextInput(attrs={'class': 'form-control form-readonly', 'readonly': 'True'}))
    price = forms.CharField(label='Предварительная цена',
                            widget=forms.TextInput(attrs={'class': 'form-control form-readonly', 'readonly': 'True'}))
    price_customer = forms.CharField(label='Сумма которую готов заплатить клиент',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):


        car = Car.objects.get(pk=self.cleaned_data['id_car'])

        Order.objects.create(
            city=self.cleaned_data['city'],
            delivery=self.cleaned_data['delivery'],
            id_customer=self.cleaned_data['customer'],
            id_worker=Worker.objects.get(full_name=self.cleaned_data['worker']),
            id_car=car,
            date_start=datetime.date.today(),
            order_status=Order.AT_WORK,
            price_customer=self.cleaned_data['price_customer']
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
        attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'data-slots': '_'}), required=False)
    comment = forms.CharField(label='Комментарий к заказу', widget=forms.Textarea(attrs={'class': 'form-control'}),
                              required=False)
    sbts = forms.FileField(label='СБТС', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                           required=False)
    export_certificate = forms.FileField(label='Экспортный сертификат', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                           required=False)
    ptd = forms.FileField(label='ПТС', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    contract_japan = forms.FileField(label='Договор купли продажи из ЯП',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    client_contract = forms.FileField(label='Договор с клиентом',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    def_ved = forms.FileField(label='Дефектная ведомость',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    consignment = forms.FileField(label='Коносамент',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    received_ptd = forms.FileField(label='Полученная ПТД',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    invoice = forms.FileField(label='Инвойс',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    payment_order = forms.FileField(label='Платежное поручение',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    price = forms.CharField(label='Рассчитанная цена',
                            widget=forms.TextInput(attrs={'class': 'form-control form-readonly', 'readonly': 'True'}),
                            required=False)
    price_for_buhgalter = forms.CharField(label='Цена покупки машины из договора купли прождажи',
                                          widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    export_certificate_number = forms.CharField(label='Номер экспортного сертификата',
                                          widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    power = forms.CharField(label='Мощность машины в л.с.', widget=forms.TextInput(attrs={'class': 'form-control'}),
                            required=False)
    photos = forms.FileField(label='Фото',
                               widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)

    def save(self, commit=True):
        order = Order.objects.filter(id_order=self.cleaned_data['id_order'])
        if self.cleaned_data['date_end'] != '':
            order.update(date_end=self.cleaned_data['date_end'])

        order.update(
            comment=self.cleaned_data['comment'],
            price=self.cleaned_data['price'],
            export_certificate_number=self.cleaned_data['export_certificate_number'],
        )
        customer = order[0].id_customer
        customer.telephone = self.cleaned_data['telephone']
        customer.save()


class CustomerForm(forms.Form):
    first_name_client = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name_client = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    patronymic_client = forms.CharField(label='Отчество', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.DateInput(
        attrs={'class': 'form-control'}))
    place_of_birth = forms.CharField(label='Место рождения', widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_series = forms.CharField(label='Серия паспорта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_number = forms.CharField(label='Номер паспорта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_department_code = forms.CharField(label='Код подразделения',
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    passport_department_name = forms.CharField(label='Кем выдан',
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Зарегистрирован по адресу', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_issue = forms.DateField(label='Дата выдачи паспорта', widget=forms.DateInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control'}))
    inn = forms.FileField(label='ИНН', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    passport = forms.FileField(label='Паспорт', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)
    registration = forms.FileField(label='Прописка', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}), required=False)

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
            telephone=self.cleaned_data['telephone'],
            address=self.cleaned_data['address'],
            date_of_issue=self.cleaned_data['date_of_issue'],
        )
        return customer.pk

    def update_customer(self, customer_id):
        customer = Customer.objects.filter(pk=customer_id)
        print(customer)
        customer.update(
            first_name_client=self.cleaned_data['first_name_client'],
            last_name_client=self.cleaned_data['last_name_client'],
            patronymic_client=self.cleaned_data['patronymic_client'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            place_of_birth=self.cleaned_data['place_of_birth'],
            passport_series=self.cleaned_data['passport_series'],
            passport_number=self.cleaned_data['passport_number'],
            passport_department_code=self.cleaned_data['passport_department_code'],
            passport_department_name=self.cleaned_data['passport_department_name'],
            telephone=self.cleaned_data['telephone'],
            address=self.cleaned_data['address'],
            date_of_issue=self.cleaned_data['date_of_issue'],
        )


class InvoiceForm(forms.Form):
    id_invoice = forms.IntegerField(label='ID',
                                    widget=forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-control'}))
    payer = forms.CharField(label='Плательщик', widget=forms.TextInput(attrs={'class': 'form-control'}))
    seller = forms.CharField(label='Получатель', widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_form = forms.CharField(label='Дата формирования',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))
    date_pay = forms.CharField(label='Дата оплаты',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))
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
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))
    date_pay = forms.CharField(label='Дата оплаты',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}))
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


class DutyForm(forms.Form):
    volume_first = forms.DecimalField(label='Объем двигателя от', decimal_places=2, max_digits=5,
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    date_of_action = forms.DateField(label='Действует от', widget=forms.DateInput(
                                    attrs={'class': 'form-control'}))
    volume_last = forms.DecimalField(label='Объем двигателя до', decimal_places=2, max_digits=5,
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    coefficient_less_3 = forms.DecimalField(label='До 3 лет', decimal_places=2, max_digits=5,
                                            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    coefficient_more_3 = forms.DecimalField(label='Старше 3 лет', decimal_places=2, max_digits=5,
                                            widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def save(self):
        Duty.objects.create(
            date_of_action=self.cleaned_data['date_of_action'],
            volume_first=self.cleaned_data['volume_first'],
            volume_last=self.cleaned_data['volume_last'],
            coefficient_less_3=self.cleaned_data['coefficient_less_3'],
            coefficient_more_3=self.cleaned_data['coefficient_more_3']
        )

    def update(self, duty_id):
        duty = Duty.objects.filter(pk=duty_id)
        duty.update(
            date_of_action=self.cleaned_data['date_of_action'],
            volume_first=self.cleaned_data['volume_first'],
            volume_last=self.cleaned_data['volume_last'],
            coefficient_less_3=self.cleaned_data['coefficient_less_3'],
            coefficient_more_3=self.cleaned_data['coefficient_more_3'],
        )

        print('Обновляем')


class PriceForm(forms.Form):
    price_first_car = forms.IntegerField(label='Цена машины от',
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    price_last_car = forms.IntegerField(label='Цена машины до',
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    price_transportation = forms.IntegerField(label='Цена перевозки',
                                              widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def save(self):
        Price.objects.create(
            price_first_car=self.cleaned_data['price_first_car'],
            price_last_car=self.cleaned_data['price_last_car'],
            price_transportation=self.cleaned_data['price_transportation'],
        )

    def update(self, price_id):
        price = Price.objects.filter(pk=price_id)
        price.update(
            price_first_car=self.cleaned_data['price_first_car'],
            price_last_car=self.cleaned_data['price_last_car'],
            price_transportation=self.cleaned_data['price_transportation'],
        )


class CustomsDutyForm(forms.Form):
    type = forms.ChoiceField(label='Возраст машины', choices=CustomsDuty.TYPE_CHOICE,
                             widget=forms.Select(attrs={'class': 'custom-select'}))
    date_of_action = forms.DateField(label='Действует от', widget=forms.DateInput(
        attrs={'class': 'form-control'}))
    value_first = forms.IntegerField(label='От значения',
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    value_last = forms.IntegerField(label='До Значения',
                                    widget=forms.NumberInput(attrs={'class': 'form-control'}))
    bet = forms.DecimalField(label='Ставка за 1 куб. см.', decimal_places=2, max_digits=10,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def save(self):
        CustomsDuty.objects.create(
            date_of_action=self.cleaned_data['date_of_action'],
            type=self.cleaned_data['type'],
            value_first=self.cleaned_data['value_first'],
            value_last=self.cleaned_data['value_last'],
            bet=self.cleaned_data['bet'],
        )

    def update(self, customs_duty_id):
        customs_duty = CustomsDuty.objects.filter(pk=customs_duty_id)
        customs_duty.update(
            date_of_action=self.cleaned_data['date_of_action'],
            type=self.cleaned_data['type'],
            value_first=self.cleaned_data['value_first'],
            value_last=self.cleaned_data['value_last'],
            bet=self.cleaned_data['bet'],
        )


class ExciseForm(forms.Form):
    date_of_action = forms.DateField(label='Действует от', widget=forms.DateInput(
        attrs={'class': 'form-control'}))
    power_first_car = forms.IntegerField(label='Мощность двигателя от',
                                         widget=forms.NumberInput(attrs={'class': 'form-control'}))
    power_last_car = forms.IntegerField(label='Мощность двигателя до',
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False)
    bet = forms.IntegerField(label='Цена за 1 л.с. в р.',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def save(self):
        Excise.objects.create(
            date_of_action=self.cleaned_data['date_of_action'],
            power_first_car=self.cleaned_data['power_first_car'],
            power_last_car=self.cleaned_data['power_last_car'],
            bet=self.cleaned_data['bet'],
        )

    def update(self, excise_id):
        excise = Excise.objects.filter(pk=excise_id)
        excise.update(
            date_of_action=self.cleaned_data['date_of_action'],
            power_first_car=self.cleaned_data['power_first_car'],
            power_last_car=self.cleaned_data['power_last_car'],
            bet=self.cleaned_data['bet'],
        )


class TransportCompanyForm(forms.Form):
    title = forms.CharField(label='Название транспортной компании',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    number_contract = forms.CharField(label='Номер договора с ТК',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    contract = forms.FileField(label='Договор с ТК', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
                               required=False)

    def save(self):
        TransportCompany.objects.create(
            title=self.cleaned_data['title'],
            contract=self.cleaned_data['contract'],
            number_contract=self.cleaned_data['number_contract'],
        )

    def update(self, transport_company_id, contract):
        print(contract)
        transport_company = TransportCompany.objects.filter(pk=transport_company_id)
        transport_company.update(
            title=self.cleaned_data['title'],
            number_contract=self.cleaned_data['number_contract'],
            contract=contract,
        )


class TransportCompanyPriceForm(forms.Form):
    place = forms.CharField(label='Место перевозки',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.CharField(label='Цена перевозки',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, tk_id):
        tk = TransportCompany.objects.get(pk=tk_id)
        TransportCompanyPrice.objects.create(
            id_transport_company=tk,
            place=self.cleaned_data['place'],
            price=self.cleaned_data['price'],
        )
        return

    def update(self, price_id):
        tk_price = TransportCompanyPrice.objects.filter(pk=price_id)
        tk_price.update(
            place=self.cleaned_data['place'],
            price=self.cleaned_data['price'],
        )
        return

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver


class PhotoCar(models.Model):
    id_photo = models.AutoField(primary_key=True)
    id_car = models.ForeignKey('Car', on_delete=models.CASCADE)
    photo = models.TextField()


class Invoice(models.Model):
    id_invoice = models.AutoField(primary_key=True)
    payer = models.TextField()
    seller = models.TextField()
    date_form = models.TextField()
    date_pay = models.TextField()
    sum = models.IntegerField()
    check_document = models.TextField()  # Ссылка на pdf
    assigning = models.TextField()
    scan = models.TextField()  # Ссылка на pdf

    # choice
    Japan = 'Оплата авто в Японии'
    Transportation = 'Оплата услуг ТК'
    Customs = 'Оплата таможенного взноса(ПТД)'
    Laboratory = 'Оплата услуг лаборатории(СБТС)'
    Company = 'Оплата услуг компании'
    type_choice = [
        (Japan, 'Оплата авто в Японии'),
        (Transportation, 'Оплата услуг ТК'),
        (Customs, 'Оплата таможенного взноса(ПТД)'),
        (Laboratory, 'Оплата услуг лаборатории(СБТС)'),
        (Company, 'Оплата услуг компании'),
    ]
    type = models.TextField(choices=type_choice)

    def get_absolute_url_invoice(self):
        return reverse('invoice', kwargs={'invoice_id': self.pk})


class Trans(models.Model):
    id_trans = models.AutoField(primary_key=True)
    id_invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
    trans_comp = models.TextField()
    departure_point = models.TextField()
    destination_point = models.TextField()
    date_form = models.DateField()
    date_shipment = models.DateField()
    date_receive = models.DateField()


class Duty(models.Model):
    volume_first = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    volume_last = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    coefficient_less_3 = models.DecimalField(max_digits=5, decimal_places=2)
    coefficient_more_3 = models.DecimalField(max_digits=5, decimal_places=2)

    def get_absolute_url_duty(self):
        return reverse('duty', kwargs={'duty_id': self.pk})


class Price(models.Model):
    price_first_car = models.IntegerField(null=True, blank=True)
    price_last_car = models.IntegerField(null=True, blank=True)
    price_transportation = models.IntegerField(null=True, blank=True)

    def get_absolute_url_price(self):
        return reverse('price', kwargs={'price_id': self.pk})


class Excise(models.Model):
    power_first_car = models.IntegerField(null=True, blank=True)
    power_last_car = models.IntegerField(null=True, blank=True)
    bet = models.IntegerField(null=True, blank=True)

    def get_absolute_url_excise(self):
        return reverse('excise', kwargs={'excise_id': self.pk})


class TransportCompany(models.Model):
    title = models.TextField(null=True, blank=True)
    contract = models.FileField(null=True, upload_to='transport_contract/', blank=True)

    def get_absolute_url_transport_company(self):
        return reverse('transport_company', kwargs={'transport_company_id': self.pk})


class TransportCompanyPrice(models.Model):
    id_transport_company = models.ForeignKey('TransportCompany', on_delete=models.CASCADE)
    place = models.TextField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)


class CustomsDuty(models.Model):
    from_0 = 'От 0 до 3 лет'
    from_3 = 'От 3 до 5 лет'
    from_5 = 'От 5 лет'
    TYPE_CHOICE = [
        (from_0, 'От 0 до 3 лет'),
        (from_3, 'От 3 до 5 лет'),
        (from_5, 'От 5 лет'),
    ]
    #     job_title = models.TextField(choices=JOB_CHOICE)
    type = models.TextField(choices=TYPE_CHOICE)
    value_first = models.IntegerField(null=True, blank=True)
    value_last = models.IntegerField(null=True, blank=True)
    bet = models.DecimalField(max_digits=10, decimal_places=2)

    def get_absolute_url_customs_duty(self):
        return reverse('customs_duty', kwargs={'customs_duty_id': self.pk})


class Order(models.Model):
    # неоплачен, оплачен
    id_order = models.AutoField(primary_key=True)
    # клиент
    id_customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    id_worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    status = models.TextField(null=True, blank=True)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True)
    id_car = models.ForeignKey('Car', on_delete=models.CASCADE)
    sbts = models.FileField(null=True, upload_to='sbts/', blank=True)
    ptd = models.FileField(null=True, upload_to='ptd/', blank=True)
    price = models.TextField(max_length=5, null=True, blank=True)

    # order_status = models.TextField(choices=ORDER_STATUS)

    def get_absolute_url_order(self):
        return reverse('order_in_orders', kwargs={'order_id': self.pk})

    def __str__(self):
        return str(self.id_order)


class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    first_name_client = models.TextField()
    last_name_client = models.TextField()
    patronymic_client = models.TextField()
    date_of_birth = models.TextField()
    place_of_birth = models.TextField()
    passport_series = models.TextField()
    passport_number = models.TextField()
    passport_department_code = models.TextField()
    passport_department_name = models.TextField()
    telephone = models.TextField()

    def __str__(self):
        return str(self.last_name_client)


class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    auc_link = models.TextField(null=True)
    title = models.TextField(null=True)

    # auction_data
    auc_name = models.TextField(null=True)
    auc_number = models.TextField(null=True)
    auc_date = models.DateField(null=True)

    # car_options
    year_car = models.TextField(null=True)
    mileage = models.TextField(null=True)
    color = models.TextField(null=True)
    options = models.TextField(null=True)
    the_body = models.TextField(null=True)
    volume = models.TextField(null=True)
    cpp = models.TextField(null=True)
    estimation = models.TextField(null=True)

    # content
    cooling = models.TextField(null=True)
    set = models.TextField(null=True)
    result = models.TextField(null=True)
    start_price = models.TextField(null=True)
    transmission = models.TextField(null=True)
    location_auction = models.TextField(null=True)
    year = models.TextField(null=True)
    alt_color = models.TextField(null=True)
    condition = models.TextField(null=True)
    fuel = models.TextField(null=True)
    equipment = models.TextField(null=True)
    deadline_for_the_price_offer = models.TextField(null=True)
    day_of_the_event = models.TextField(null=True)
    number_of_sessions = models.TextField(null=True)

    auc_list = models.TextField(null=True)

    price = models.TextField(null=True)

    def get_absolute_url_car(self):
        return reverse('car', kwargs={'car_id': self.pk})

    def get_absolute_url_order(self):
        return reverse('order', kwargs={'car_id': self.pk})

    def get_fields(self):
        poles = list()
        for field in Car._meta.fields:
            match field.name:
                case 'year_car':
                    poles.append(['Год', field.value_to_string(self)])
                case 'mileage':
                    poles.append(['Пробег', field.value_to_string(self)])
                case 'alt_color':
                    poles.append(['Цвет', field.value_to_string(self)])
                case 'options':
                    poles.append(['Опции', field.value_to_string(self)])
                case 'the_body':
                    poles.append(['Кузов', field.value_to_string(self)])
                case 'volume':
                    poles.append(['Объем', field.value_to_string(self)])
                case 'cpp':
                    poles.append(['КПП', field.value_to_string(self)])
                case 'estimation':
                    poles.append(['Оценка', field.value_to_string(self)])
                case 'cooling':
                    poles.append(['Охлаждение', field.value_to_string(self)])
                case 'set':
                    poles.append(['Комплектация', field.value_to_string(self)])
                case 'result':
                    poles.append(['Результат', field.value_to_string(self)])
                case 'start_price':
                    poles.append(['Стартовая цена', field.value_to_string(self)])
                case 'transmission':
                    poles.append(['Коробка передач', field.value_to_string(self)])
                case 'location_auction':
                    poles.append(['Место проведения', field.value_to_string(self)])
                case 'location_auction':
                    poles.append(['Место проведения', field.value_to_string(self)])
                case 'condition':
                    poles.append(['Состояние аукциона', field.value_to_string(self)])
                case 'fuel':
                    poles.append(['Топливо', field.value_to_string(self)])
                case 'equipment':
                    poles.append(['Оборудование', field.value_to_string(self)])
                case 'deadline_for_the_price_offer':
                    poles.append(['Конечный срок предложения цены', field.value_to_string(self)])
                case 'day_of_the_event':
                    poles.append(['День проведения', field.value_to_string(self)])
                case 'number_of_sessions':
                    poles.append(['Количество проведений', field.value_to_string(self)])
                case 'price':
                    poles.append(['Предполагаемая цена', field.value_to_string(self) + ' р.'])
        return poles

    def __str__(self):
        return str(self.title)


class Worker(AbstractUser):
    MANAGER = 'Менеджер'
    LOGIST = 'Логист'
    HR = 'HR'
    ACCOUNTANT = 'Бухгалтер'
    OPERATIVNIK = 'Оперативник'
    JOB_CHOICE = [
        (MANAGER, 'Менеджер'),
        (LOGIST, 'Логист'),
        (HR, 'HR'),
        (ACCOUNTANT, 'Бухгалтер'),
        (OPERATIVNIK, 'Оперативник')
    ]

    full_name = models.TextField()
    job_title = models.TextField(choices=JOB_CHOICE)
    phone_number = models.TextField()
    passport = models.TextField(unique=True)

    def __str__(self):
        return str(self.full_name)

    def get_absolute_url_worker(self):
        return reverse('workers_card', kwargs={'worker_id': self.id})

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


@receiver(pre_save, sender=Worker)
def set_worker_id(sender, instance, **kwargs):
    if not instance.id:
        # Получаем максимальное значение worker_id, если оно есть, иначе устанавливаем 0
        max_id = Worker.objects.aggregate(models.Max('id'))['id__max'] or 0
        instance.id = max_id + 1

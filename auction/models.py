from django.db import models
from django.urls import reverse


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


class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    # клиент
    id_customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    id_worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    status = models.TextField(null=True)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    comment = models.TextField(null=True)
    id_car = models.ForeignKey('Car', on_delete=models.CASCADE)
    sbts = models.FileField(null=True, upload_to='sbts/')
    ptd = models.FileField(null=True, upload_to='ptd/')
    price = models.TextField(max_length=5, null=True, blank=True)

    def get_absolute_url_order(self):
        return reverse('order_in_orders', kwargs={'order_id': self.pk})


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

    def get_absolute_url_car(self):
        return reverse('car', kwargs={'car_id': self.pk})

    def get_absolute_url_order(self):
        print('ХОП')
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
        return poles


class Worker(models.Model):
    MANAGER = 'Клиент-менеджер'
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
    id_worker = models.AutoField(primary_key=True)
    username = models.TextField(unique=True)
    full_name = models.TextField()
    job_title = models.TextField(choices=JOB_CHOICE)
    phone_number = models.TextField()
    passport = models.TextField(unique=True)
    password = models.TextField()

    def __str__(self):
        return str(self.full_name)

    def get_absolute_url_worker(self):
        return reverse('workers_card', kwargs={'worker_id': self.pk})

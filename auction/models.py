from django.db import models


class PhotoCar(models.Model):
    id_photo = models.AutoField(primary_key=True)
    id_car = models.ForeignKey('Car', on_delete=models.CASCADE)
    photo = models.TextField()


class Invoices(models.Model):
    id_invoice = models.AutoField(primary_key=True)
    payer = models.TextField()
    receipent = models.TextField()
    date_form = models.DateField()
    date_pay = models.DateField()
    sum = models.IntegerField()
    check_to_client = models.TextField()
    type = models.CharField(max_length=50)  # Уточните ENUM-тип


class Trans(models.Model):
    id_trans = models.AutoField(primary_key=True)
    id_invoice = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    trans_comp = models.TextField()
    departure_point = models.TextField()
    destination_point = models.TextField()
    date_form = models.DateField()
    date_shipment = models.DateField()
    date_receive = models.DateField()


class Order(models.Model):
    id_order = models.AutoField(primary_key=True)
    id_customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    id_worker = models.ForeignKey('Worker', on_delete=models.CASCADE)
    id_invoice_comp = models.ForeignKey(Invoices, on_delete=models.CASCADE)
    status = models.TextField()
    date_start = models.DateField()
    date_end = models.DateField()
    comment = models.TextField()
    id_car = models.ForeignKey('Car', on_delete=models.CASCADE)


class Customer(models.Model):
    id_customer = models.AutoField(primary_key=True)
    full_name = models.TextField()
    passport_num = models.TextField()
    tel_num = models.TextField()


class Car(models.Model):
    id_car = models.AutoField(primary_key=True)
    auc_link = models.TextField()
    title = models.TextField()

    # auction_data
    auc_name = models.TextField()
    auc_number = models.TextField()
    auc_date = models.DateField()

    # car_options
    year_car = models.TextField()
    mileage = models.TextField()
    color = models.TextField()
    options = models.TextField()
    the_body = models.TextField()
    volume = models.TextField()
    cpp = models.TextField()
    estimation = models.TextField()

    # content
    cooling = models.TextField()
    set = models.TextField()
    result = models.TextField()
    start_price = models.TextField()
    transmission = models.TextField()
    location_auction = models.TextField()
    year = models.TextField()
    alt_color = models.TextField()
    condition = models.TextField()
    fuel = models.TextField()
    equipment = models.TextField()
    deadline_for_the_price_offer = models.TextField()
    day_of_the_event = models.TextField()
    number_of_sessions = models.TextField()

    auc_list = models.TextField()


class CarForPage(models.Model):
    id_car = models.AutoField(primary_key=True)
    title = models.TextField()
    auction_data = models.TextField()
    car_options = models.TextField()
    content = models.TextField()


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
    full_name = models.TextField(unique=True)
    job_title = models.TextField(choices=JOB_CHOICE)
    password = models.TextField()

    def __str__(self):
        return str(self.full_name)

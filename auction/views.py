# В парсер добавлены методы гет(для нормального вывода формы) и пост(для парсинга)
# Файл parser.py можно удалить, парсер будет находиться тут или в отдельном приложении, что, наверное, грамотнее
# После парсинга данные выходят в очень некрасивом виде, можно попробовать выводить их словарем
# После парсинга сделал так, чтобы данные выводились на стричку car
# Вывод сделал коряво - car не внесена в url и не имеет своего класса. В будущем надо исправить
# Для норм вывода надо сделать метод гет в классе CarPageView и, наверное, сделать модель
import datetime
import os

from bs4 import BeautifulSoup
import requests
import django.http
from django.views.generic import TemplateView
from django.shortcuts import render
from openpyxl.reader.excel import load_workbook

from .models import Car, PhotoCar, Worker, Order, Invoice
from .forms import ParserForm, RegistrationForm, LoginForm, LogoutForm, OrderForm, OrderInOrdersForm, InvoiceForm, NewInvoiceForm
from django.contrib import messages
from django.conf import settings
import pandas as pd


class HomePageView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            return render(request, self.template_name)


class WorkersPageView(TemplateView):
    template_name = "workers.html"

    def get(self, request, *args, **kwargs):
        workers = Worker.objects.all()
        return render(request, 'workers.html', {'workers': workers})


class WorkersCardPageView(TemplateView):
    template_name = "worker_card.html"

    def get(self, request, *args, **kwargs):
        worker = Worker.objects.get(id_worker=kwargs.get('worker_id'))
        worker_data = Worker.objects.all()
        form = RegistrationForm()
        form.fields['username'].widget.attrs.update({'value': worker.username})
        form.fields['full_name'].widget.attrs.update({'value': worker.full_name})
        # Вот тут хуй знает как сделать не нашел
        form.fields['job_title'].widget.attrs.update({'value': worker.job_title})
        # Вот тут хуй знает как сделать не нашел
        form.fields['passport'].widget.attrs.update({'value': worker.passport})
        form.fields['phone_num'].widget.attrs.update({'value': worker.phone_number})
        form.fields['password1'].widget.attrs.update({'value': worker.password})
        form.fields['password2'].widget.attrs.update({'value': worker.password})

        return render(request, 'worker_card.html', {'worker': worker, 'worker_data': worker_data, 'form': form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                # form.username_clean()

                form.clean_password2()
                form.update()
                messages.info(request, "Данные обновалены")
        else:
            form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})


class LoginPageView(TemplateView):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = LoginForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                if form.login_clean() == '#':
                    messages.info(request, "Данное имя пользователя не найдено")
                    return render(request, 'registration/login.html', {'form': form})
                messages.info(request, "Вход выполнен")
                return render(request, 'home.html')
        else:
            form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


class LogoutPageView(TemplateView):
    template_name = "registration/logout.html"

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = LogoutForm()
            return render(request, self.template_name, {'form': form})


class RegistrationPageView(TemplateView):
    template_name = "registration/registration.html"

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = RegistrationForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                # form.username_clean()
                if form.username_clean() == '#':
                    # message = messages.info(request, 'Your password has been changed successfully!')
                    messages.info(request, "Данное имя пользователя уже используется")
                    return render(request, 'registration/registration.html', {'form': form})
                if form.passport_clean() == '#':
                    # message = messages.info(request, 'Your password has been changed successfully!')
                    messages.info(request, "Пользователь с таким паспортом уже существует")
                    return render(request, 'registration/registration.html', {'form': form})
                form.clean_password2()
                form.save()
                messages.info(request, "Пользователь зарегистрирован")
        else:
            form = RegistrationForm()
        return render(request, 'registration/registration.html', {'form': form})


class OrderInOrdersPageView(TemplateView):
    template_name = 'order_in_orders.html'

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id_order=kwargs['order_id'])
        print(order.ptd == '')
        print(order.sbts == '')

        form = OrderInOrdersForm()

        form.fields['id_order'].widget.attrs.update({'value': order.id_order})
        form.fields['first_name_client'].widget.attrs.update({'value': order.id_customer.first_name_client})
        form.fields['last_name_client'].widget.attrs.update({'value': order.id_customer.last_name_client})
        form.fields['patronymic_client'].widget.attrs.update({'value': order.id_customer.patronymic_client})
        form.fields['telephone'].widget.attrs.update({'value': order.id_customer.telephone})
        form.fields['date_start'].widget.attrs.update({'value': order.date_start})
        form.fields['sbts'].widget.initial_text = ''
        form.fields['sbts'].widget.input_text = 'Заменить'
        form.fields['ptd'].widget.initial_text = ''
        form.fields['ptd'].widget.input_text = 'Заменить'
        form.fields['ptd'].widget.clear_checkbox_label = ''
        form.fields['sbts'].widget.clear_checkbox_label = ''
        if order.date_end is not None:
            form.fields['date_end'].widget.attrs.update({'value': order.date_end, 'readonly': 'True'})
        if order.comment is not None:
            form.fields['comment'].initial = order.comment
        if order.sbts is not None:
            form.fields['sbts'].initial = order.sbts
        if order.ptd is not None:
            form.fields['ptd'].initial = order.ptd
        return render(request, self.template_name, {'order': order, 'form': form})

    def post(self, request, *args, **kwargs):
        print(request.FILES)
        if request.method == 'POST':
            form = OrderInOrdersForm(request.POST, request.FILES)
            if form.is_valid():

                order = Order.objects.filter(id_order=form.cleaned_data['id_order'])
                order = order[0]
                # is_initial
                print(form.initial)
                print(form.cleaned_data['date_end'])
                # print(form.fields['ptd'].initial)

                if order.ptd == '':
                    order.ptd = request.FILES.get('ptd')
                else:
                    order.ptd = order.ptd

                if order.sbts == '':
                    order.sbts = request.FILES.get('sbts')
                else:
                    order.sbts = order.sbts

                order.save()

                messages.info(request, "Заказ изменен")
                form.save()
            else:
                messages.info(request, "Чета блять сломалось")
                for field in form:
                    print("Field Error:", field.name, field.errors)
        else:
            form = OrderForm()
        orders = Order.objects.filter(date_end=None)
        return render(request, 'orders.html', {"orders": orders})


class OrdersPageView(TemplateView):
    template_name = "orders.html"

    def get(self, request, *args, **kwargs):
        print('Пришел запрос')
        orders = Order.objects.filter(date_end=None)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})


class OrderPageView(TemplateView):
    template_name = "order.html"

    def get(self, request, *args, **kwargs):
        car = Car.objects.get(id_car=kwargs.get('car_id'))
        form = OrderForm()
        photo = PhotoCar.objects.filter(id_car=kwargs.get('car_id'))[:1][0].photo
        form.fields['id_car'].widget.attrs.update({'value': car.id_car})
        return render(request, 'order.html', {'car': car, 'form': form, 'photo': photo})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, "Пользователь зарегистрирован")
            else:
                messages.info(request, "Чета блять сломалось")
                for field in form:
                    print("Field Error:", field.name, field.errors)
        else:
            form = OrderForm()

        orders = Order.objects.filter(date_end=None)
        print(orders)
        return render(request, 'orders.html', {'orders': orders})


class CatalogPageView(TemplateView):

    def get(self, request, *args, **kwargs):
        cars = Car.objects.all()
        cars = Car.objects.filter(auc_date__gte=datetime.date.today())

        for el in cars:
            el.image = PhotoCar.objects.filter(id_car=el.id_car)[:1][0].photo

        return render(request, 'catalog.html', {'cars': cars})


class CarPageView(TemplateView):
    template_name = "car.html"

    def get(self, request, *args, **kwargs):
        car = Car.objects.get(id_car=kwargs.get('car_id'))
        photo = PhotoCar.objects.filter(id_car=car)

        # Достаем данные из excel
        file_path = 'cars_price.xlsx'
        workbook = load_workbook(filename=file_path)

        models_list = workbook.worksheets[1]
        mark_list = workbook.worksheets[0]

        models = []
        skip_first_row = False
        for row in models_list.iter_rows(values_only=True, min_row=2 if skip_first_row else 1):
            model = {
                'id': row[0],
                'mark': row[1],
                'model': row[2],
                'price': row[3],
            }
            models.append(model)
        marks = []
        for row in mark_list.iter_rows(values_only=True, min_row=2 if skip_first_row else 1):
            mark = {
                'id': row[0],
                'mark': row[1]
            }
            marks.append(mark)
        print(models)
        print(marks)
        mark = marks[0]
        print(marks[0]['mark'])
        # Достаем данные из excel

        # Узнаем цену машины
        car_for_test = Car.objects.all()
        for car_test in car_for_test:
            car_title = car_test.title.split()
            is_car = False
            price = 0
            for car_for_test in models:

                # if str(marks[int(car_for_test['mark'])-1]['mark']) == 'Acura':
                #     print(car_for_test, marks[int(car_for_test['mark'])-1]['mark'], 'true', int(car_for_test['mark']))
                # print(marks[int(car_for_test['mark'])-1]['mark'], car_title[0].lower())
                if (str(car_for_test['model']).lower() == car_title[1].lower()
                        and
                        str(marks[int(car_for_test['mark'])-1]['mark']).lower() == car_title[0].lower()):
                    is_car = True
                    price = car_for_test['price']
            if is_car is False:
                price ='Нет информации о цене'

            print(car_test.title, price)


        return render(request, 'car.html', {'car': car, 'photo': photo})


class ParserPageView(TemplateView):
    template_name = "parser.html"

    def get(self, request, *args, **kwargs):
        form = ParserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        linked_list = list()
        print('Пришел пост запрос')
        if request.method == 'POST' and 'import' in request.POST:
            url = 'https://www.carwin.ru/japanauc/'
            response = requests.get(url)
            html_page = BeautifulSoup(response.text, 'lxml')
            urls_list = html_page.find('ul', 'pagination')
            urls_list = urls_list.find_all('a')

            for i in range(1, len(urls_list) + 1):

                response = requests.get(url + str(i))
                html_page = BeautifulSoup(response.text, 'lxml')
                links = html_page.find_all('a', 'pic')
                for link in links:
                    linked_list.append(link['href'])

            url = 'https://www.carwin.ru'
            print(url + linked_list[0])
            k = 0
            for link in linked_list:
                k += 1
                print(k)
                self.link_obr(url + link)

        return render(request, 'parser.html', {'response': 'success'})

    def link_obr(self, url):

        response = requests.get(url)
        html_page = BeautifulSoup(response.text, "lxml")
        number_of_auc = html_page.find('div', 'row_desc_middle')

        car = Car.objects.filter(auc_number=number_of_auc.text)

        if html_page.find('div', 'page_title') is not None and not car:

            Obj = Car_data(url)
            print(url)
            Obj.print()

            Obj.save_me_to_bd()
            del Obj
        else:

            print('Было, знаем!', url)
            # return


class Parser(object):
    html_page = None

    def __init__(self, url):
        response = requests.get(url)
        self.html_page = BeautifulSoup(response.text, "lxml")
        print(response)

    def parse_title(self):
        name = self.html_page.find('div', 'page_title').text
        return name

    def parse_auction_data(self):
        auction_data = self.html_page.find('div', 'col_left').text
        auction_data = [value for value in auction_data.split('\n') if value != '']
        return auction_data

    def parse_car_options(self):
        car_options = self.html_page.find('div', 'car_description')
        car_options = car_options.find_all('div', 'car_option')

        data_set = {'year_car': '', 'mileage': '', 'color': '', 'options': '', 'the_body': '', 'volume': '', 'cpp': '',
                    'estimation': ''}

        # Условие не трогать, работает и слава богу
        for el in range(0, len(car_options)):
            split_data_of_car = car_options[el].text.split()

            match split_data_of_car[0]:
                case 'Год':
                    if len(split_data_of_car) > 1:
                        data_set['year_car'] = split_data_of_car[1]
                case 'Пробег':
                    if len(split_data_of_car) > 1:
                        data_set['mileage'] = split_data_of_car[1]
                case 'Цвет':
                    if len(split_data_of_car) > 1:
                        data_set['color'] = split_data_of_car[1]
                case 'Опции':
                    if len(split_data_of_car) > 1:
                        data_set['options'] = split_data_of_car[1]
                case 'Кузов':
                    if len(split_data_of_car) > 1:
                        data_set['the_body'] = split_data_of_car[1]
                case 'Объем':
                    if len(split_data_of_car) > 1:
                        data_set['volume'] = split_data_of_car[1]
                case 'КПП':
                    if len(split_data_of_car) > 1:
                        data_set['cpp'] = split_data_of_car[1]
                case 'Оценка':
                    if len(split_data_of_car) > 1:
                        data_set['estimation'] = split_data_of_car[1]

        car_options = data_set
        return car_options

    def parse_content(self):
        content = self.html_page.find('div', 'content')
        content = content.find_all('td')

        data_set = {'cooling': '',
                    'set': '',
                    'result': '',
                    'start_price': '',
                    'transmission': '',
                    'location_auction': '',
                    'year': '',
                    'alt_color': '',
                    'condition': '',
                    'fuel': '',
                    'equipment': '',
                    'deadline_for_the_price_offer': '',
                    'day_of_the_event': '',
                    'number_of_sessions': ''}
        # Почему здесь по-другому, не знаю, но тоже работает и слава богу
        for el in range(0, len(content), 2):
            match content[el].text:
                case ' охлаждение ':
                    data_set['cooling'] = content[el + 1].text
                case ' комплектация ':
                    data_set['set'] = content[el + 1].text
                case ' результат ':
                    data_set['result'] = content[el + 1].text
                case ' старт ':
                    data_set['start_price'] = content[el + 1].text
                case ' коробка передач ':
                    data_set['transmission'] = content[el + 1].text
                case ' место проведения ':
                    data_set['location_auction'] = content[el + 1].text
                case ' год ':
                    data_set['year'] = content[el + 1].text
                case ' цвет ':
                    data_set['alt_color'] = content[el + 1].text
                case ' состояние ':
                    data_set['condition'] = content[el + 1].text
                case ' топливо ':
                    data_set['fuel'] = content[el + 1].text
                case ' оборудование ':
                    data_set['equipment'] = content[el + 1].text
                case ' конечный срок предложения цены ':
                    data_set['deadline_for_the_price_offer'] = content[el + 1].text
                case ' день проведения ':
                    data_set['day_of_the_event'] = content[el + 1].text
                case ' количество проведений ':
                    data_set['number_of_sessions'] = content[el + 1].text

        content = data_set
        return content

    def parse_image(self):
        image = self.html_page.find('div', 'my-gallery')
        image = image.find_all('img')
        form_data = list()

        for el in range(len(image)):
            form_data.append(image[el]['src'])
        image = form_data
        return image

    def parse_auc_list(self):
        auc_list = self.html_page.find('div', 'scheme_block')
        auc_list = auc_list.find('img')
        auc_list = auc_list['src']
        return auc_list


class Car_data(object):
    title = ''
    auction_data = ''
    car_options = ''
    content = ''
    auc_link = ''
    image = ''
    # auction_data
    auc_name = ''
    auc_number = ''
    auc_date = ''
    # car_options
    year_car = ''
    mileage = ''
    color = ''
    options = ''
    the_body = ''
    volume = ''
    cpp = ''
    estimation = ''
    # content
    cooling = ''
    set = ''
    result = ''
    start_price = ''
    transmission = ''
    location_auction = ''
    year = ''
    alt_color = ''
    condition = ''
    fuel = ''
    equipment = ''
    deadline_for_the_price_offer = ''
    day_of_the_event = ''
    number_of_sessions = ''

    auc_list = ''

    def __init__(self, url):
        parser = Parser(url)
        self.auc_link = url
        # для Car_of_page
        self.title = parser.parse_title()
        self.auction_data = parser.parse_auction_data()
        self.car_options = parser.parse_car_options()
        self.content = parser.parse_content()
        self.image = parser.parse_image()

        # для Car_data

        # auction_data
        self.auc_name = parser.parse_auction_data()[0]
        self.auc_number = parser.parse_auction_data()[1]
        self.auc_date = parser.parse_auction_data()[2]

        # car_options
        form_data = parser.parse_car_options()

        self.year_car = form_data['year_car']
        self.mileage = form_data['mileage']
        self.color = form_data['color']
        self.options = form_data['options']
        self.the_body = form_data['the_body']
        self.volume = form_data['volume']
        self.cpp = form_data['cpp']
        self.estimation = form_data['estimation']

        # content
        form_data = parser.parse_content()

        self.cooling = form_data['cooling']
        self.set = form_data['set']
        self.result = form_data['result']
        self.start_price = form_data['start_price']
        self.transmission = form_data['transmission']
        self.location_auction = form_data['location_auction']
        self.year = form_data['year']
        self.alt_color = form_data['alt_color']
        self.condition = form_data['condition']
        self.fuel = form_data['fuel']
        self.equipment = form_data['equipment']
        self.deadline_for_the_price_offer = form_data['deadline_for_the_price_offer']
        self.day_of_the_event = form_data['day_of_the_event']
        self.number_of_sessions = form_data['number_of_sessions']

        self.auc_list = parser.parse_auc_list()

    def print(self):
        print('название машины', self.title, 'аукцион', self.auction_data, 'основное про машину', self.car_options,
              'таблица', self.content, sep='\n', end='\n')
        print('картинки', self.image, end='\n')
        print(self.auc_name, self.auc_number, self.auc_date, sep='\n', end='\n')
        print(self.year_car, self.mileage, self.color, self.options, self.the_body, self.volume, self.cpp,
              self.estimation, sep='\n', end='\n')
        print(self.cooling, self.condition, self.fuel, self.equipment)

    def __del__(self):
        print('Удален')

    def save_me_to_bd(self):
        new_car_new = Car.objects.create(
            auc_link=self.auc_link,
            title=self.title,
            auc_name=self.auc_name,
            auc_number=self.auc_number,
            auc_date=self.auc_date,
            year_car=self.year_car,
            mileage=self.mileage,
            color=self.color,
            options=self.options,
            the_body=self.the_body,
            volume=self.volume,
            cpp=self.cpp,
            estimation=self.estimation,
            cooling=self.cooling,
            set=self.set,
            result=self.result,
            start_price=self.start_price,
            transmission=self.transmission,
            location_auction=self.location_auction,
            year=self.year,
            alt_color=self.alt_color,
            condition=self.condition,
            fuel=self.fuel,
            equipment=self.equipment,
            deadline_for_the_price_offer=self.deadline_for_the_price_offer,
            day_of_the_event=self.day_of_the_event,
            number_of_sessions=self.number_of_sessions,
            auc_list=self.auc_list
        )
        for el in range(len(self.image)):
            PhotoCar.objects.create(id_car=new_car_new, photo=self.image[el])

        print(new_car_new)


class BuhgalterPageView(TemplateView):
    template_name = "buhgalter/buhgalter.html"

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.all()
        print('Тут должен быть инвойс')
        print(invoices)
        return render(request, 'buhgalter/buhgalter.html', {'invoices': invoices})


class BuhgalterInvoicePageView(TemplateView):
    template_name = "buhgalter/invoice.html"

    def get(self, request, *args, **kwargs):
        invoice = Invoice.objects.get(id_invoice=kwargs.get('invoice_id'))
        invoice_data = Invoice.objects.all()
        form = InvoiceForm()
        form.fields['id_invoice'].widget.attrs.update({'value': invoice.id_invoice})
        form.fields['payer'].widget.attrs.update({'value': invoice.payer})
        form.fields['seller'].widget.attrs.update({'value': invoice.seller})
        form.fields['date_form'].widget.attrs.update({'value': invoice.date_form})
        form.fields['date_pay'].widget.attrs.update({'value': invoice.date_pay})
        form.fields['sum'].widget.attrs.update({'value': invoice.sum})
        form.fields['check_document'].widget.attrs.update({'value': invoice.check_document})
        form.fields['assigning'].widget.attrs.update({'value': invoice.assigning})
        form.fields['scan'].widget.attrs.update({'value': invoice.scan})
        form.fields['type'].widget.attrs.update({'value': invoice.type})

        return render(request, 'buhgalter/invoice.html',
                      {'invoice': invoice, 'invoice_data': invoice_data, 'form': form})

    def post(self, request, *args, **kwargs):
        invoices = Invoice.objects.all()
        if request.method == 'POST':
            form = InvoiceForm(request.POST)
            print('Валидная или инвалидная форма', form.is_valid())
            print(form.errors)
            if form.is_valid():
                form.update()
                messages.info(request, "Данные обновлены")
        else:
            form = InvoiceForm()
        return render(request, 'buhgalter/buhgalter.html', {'invoices': invoices})


class BuhgalterNewInvoicePageView(TemplateView):
    template_name = "buhgalter/new_invoice.html"

    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
            form = InvoiceForm()
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        invoices = Invoice.objects.all()
        if request.method == 'POST':
            print('Запрос пришел')
            form = NewInvoiceForm(request.POST)
            print(form.is_valid())
            print(form.errors)
            if form.is_valid():
                form.save()
                messages.info(request, "Счет на оплату сохранен")
                return render(request, 'buhgalter/new_invoice.html', {'form': form})
            # form.save()
            # messages.info(request, "Счет на оплату сохранен")
        else:
            form = NewInvoiceForm()
        return render(request, 'buhgalter/buhgalter.html', {'invoices': invoices})

# В парсер добавлены методы гет(для нормального вывода формы) и пост(для парсинга)
# Файл parser.py можно удалить, парсер будет находиться тут или в отдельном приложении, что, наверное, грамотнее
# После парсинга данные выходят в очень некрасивом виде, можно попробовать выводить их словарем
# После парсинга сделал так, чтобы данные выводились на стричку car
# Вывод сделал коряво - car не внесена в url и не имеет своего класса. В будущем надо исправить
# Для норм вывода надо сделать метод гет в классе CarPageView и, наверное, сделать модель

from django.views.generic import TemplateView
from django.shortcuts import render
from .models import Car_data, Car_for_page
from .forms import ParserForm


class HomePageView(TemplateView):
    template_name = "home.html"


# class CarPageView(TemplateView):
#     template_name = "car.html"


class ParserPageView(TemplateView):
    template_name = "parser.html"

    def get(self, request, *args, **kwargs):
        form = ParserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ParserForm(request.POST)
            if form.is_valid():
                url1 = 'https://www.carwin.ru/japanauc/see/'
                url = form.cleaned_data['url_parser_field']
                for i in range(945500000, 945500005):
                    Obj = Car_data(url1 + str(i))
                    print(url1 + str(i))
                    Obj.print()
                    render(request, "car.html",
                           {'title': Obj.title, 'auction_data': Obj.auction_data, 'car_options': Obj.car_options,
                            'content': Obj.content, 'image': Obj.image, 'range': range(5)})
                    Obj.save_me_to_bd()
                    del Obj
                    # return

        else:
            form = ParserForm()
        return render(request, 'parser.html', {'form': form})


class Parser(object):
    html_page = None

    def __init__(self, url):
        from bs4 import BeautifulSoup
        import requests

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
        form_data = list()
        data_set = {}

        # Условие не трогать, работает и слава богу
        for el in range(0, len(car_options)):
            split_data_of_car = car_options[el].text.split()

            match split_data_of_car[0]:
                case 'Год':
                    data_set['year_car'] = split_data_of_car[1]
                case 'Пробег':
                    data_set['mileage'] = split_data_of_car[1]
                case 'Цвет':
                    data_set['color'] = split_data_of_car[1]
                case 'Опции':
                    data_set['options'] = split_data_of_car[1]
                case 'Кузов':
                    data_set['the_body'] = split_data_of_car[1]
                case 'Объем':
                    data_set['volume'] = split_data_of_car[1]
                case 'КПП':
                    data_set['cpp'] = split_data_of_car[1]
                case 'Оценка':
                    data_set['estimation'] = split_data_of_car[1]

            print('ДАТА СЕТ', data_set['year_car'])

        car_options = data_set
        return car_options

    def parse_content(self):
        content = self.html_page.find('div', 'content')
        content = content.find_all('td')
        form_data = list()
        # Почему здесь по-другому, не знаю, но тоже работает и слава богу
        for el in range(0, len(content), 2):
            form_data.append([content[el].text, content[el + 1].text])
        content = form_data
        return content

    def parse_image(self):

        image = self.html_page.find('div', 'my-gallery')
        image = image.find_all('img')
        form_data = list()

        for el in range(len(image)):
            form_data.append(image[el]['src'])
        image = form_data
        return image


class Car_data(object):
    url = ''
    title = ''
    auction_data = ''
    car_options = ''
    content = ''
    image = ''

    auc_name = ''
    auc_number = ''
    auc_date = ''

    year_car = ''
    mileage = ''
    color = ''
    options = ''
    the_body = ''
    volume = ''
    cpp = ''
    estimation = ''
    def __init__(self, url):
        parser = Parser(url)

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
        form_data = parser.parse_auction_data()
        # self.year_car = form_data['year_car']
        # self.mileage = form_data['mileage']
        # self.color = form_data['color']
        # self.options = form_data['options']
        # self.the_body = form_data['the_body']
        # self.volume = form_data['volume']
        # self.cpp = form_data['cpp']
        # self.estimation = form_data['estimation']

    def print(self):
        print('название машины', self.title, 'аукцион', self.auction_data, 'основное про машину', self.car_options,
              'таблица', self.content, sep='\n', end='\n')
        print('картинки', self.image, end='\n')
        print(self.auc_name, self.auc_number, self.auc_date, sep='\n', end='\n')
        # print(self.year_car, self.mileage, self.color, self.options, self.the_body, self.volume, self.cpp, self.estimation, sep='\n', end='\n')

    def __del__(self):
        print('Удален')

    def save_me_to_bd(self):
        new_car = Car_for_page.objects.create(title=self.title, auction_data=self.auction_data, content=self.content, car_options=self.car_options)
        print(new_car)



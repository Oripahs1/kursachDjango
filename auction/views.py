# В парсер добавлены методы гет(для нормального вывода формы) и пост(для парсинга)
# Файл parser.py можно удалить, парсер будет находиться тут или в отдельном приложении, что, наверное, грамотнее
# После парсинга данные выходят в очень некрасивом виде, можно попробовать выводить их словарем
# После парсинга сделал так, чтобы данные выводились на стричку car
# Вывод сделал коряво - car не внесена в url и не имеет своего класса. В будущем надо исправить
# Для норм вывода надо сделать метод гет в классе CarPageView и, наверное, сделать модель

from django.views.generic import TemplateView
from django.shortcuts import render

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
                url = form.cleaned_data['url_parser_field']
                Obj = Car_data(url)
                Obj.print()
                return render(request, "car.html",
                              {'title': Obj.title, 'auction_data': Obj.auction_data, 'car_options': Obj.car_options,
                               'content': Obj.content, 'range': range(4)})
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

        # Условие не трогать, работает и слава богу
        for el in range(0, len(car_options)):
            split_data_of_car = car_options[el].text.split()
            form_data.append([split_data_of_car[0], split_data_of_car[1]])
        car_options = form_data
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


class Car_data(object):
    url = ''
    title = ''
    auction_data = ''
    car_options = ''
    content = ''

    def __init__(self, url):
        parser = Parser(url)
        self.title = parser.parse_title()
        self.auction_data = parser.parse_auction_data()
        self.car_options = parser.parse_car_options()
        self.content = parser.parse_content()

    def print(self):
        print('название машины', self.title, 'аукцион', self.auction_data, 'основное про машину', self.car_options,
              'таблица', self.content, sep='\n', end='\n')

# url = 'https://www.carwin.ru/japanauc/see/945389787'
# Obj = Car_data(url)
# Obj.print()

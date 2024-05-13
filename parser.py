# Если собрался что-то менять - спроси Германа
# Тут мы парсим данные со странички по ссылке
#
# Есть два класса:
# Parser - включает в себя логику и сам парсер
#
# Car_data - инициализирует процесс парсинга и собирает в себя данные
#
# В идеале в конце должен быть экземпляр класса Car_data, со всеми нужными данными внутри

from bs4 import BeautifulSoup
import requests


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
        auction_data = auction_data.split('\n')
        return auction_data

    def parse_car_options(self):

        car_options = self.html_page.find('div', 'car_description')
        car_options = car_options.find_all('div', 'car_option')
        form_data = [[0] * 2 for i in range(len(car_options))]

        # Условие не трогать, работает и слава богу
        k = 0
        for el in range(0, len(car_options)):
            split_data_of_car = car_options[el].text.split()
            form_data[k][0] = split_data_of_car[0]
            form_data[k][1] = split_data_of_car[1]
            k += 1
        car_options = form_data
        return car_options

    def parse_content(self):

        content = self.html_page.find('div', 'content')
        content = content.find_all('td')
        form_data = [[0] * 2 for i in range(len(content) // 2)]

        # Почему здесь по-другому, не знаю, но тоже работает и слава богу
        k = 0
        for el in range(0, len(content), 2):
            form_data[k][0] = content[el].text

            form_data[k][1] = content[el + 1].text
            k += 1

        content = form_data
        return content

    def parse_image(self):

        image = self.html_page.find('div', 'my-gallery')
        image = image.find_all('img')

        form_data = [[0] * 1 for i in range(len(image))]

        k = 0
        for el in range(len(image)):
            form_data[k] = image[el]['src']
            k += 1
        image = form_data
        return image


class Car_data(object):
    url = ''
    title = ''
    auction_data = ''
    car_options = ''
    content = ''
    image = ''

    def __init__(self, url):
        parser = Parser(url)

        self.title = parser.parse_title()
        self.auction_data = parser.parse_auction_data()
        self.car_options = parser.parse_car_options()
        self.content = parser.parse_content()
        self.image = parser.parse_image()

    def print(self):
        print([self.title, self.auction_data, self.car_options, self.content, self.image])
        print(self.image)


url = 'https://www.carwin.ru/japanauc/see/945389787'
Obj = Car_data(url)
Obj.print()

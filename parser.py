from bs4 import BeautifulSoup
import requests

url = 'https://www.carwin.ru/japanauc/see/945389787'
response = requests.get(url)
print(response)
bs = BeautifulSoup(response.text,"lxml")
# print(bs)
temp = bs.find('div', 'content')
# print(temp)
print(temp.text)

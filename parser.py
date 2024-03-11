from bs4 import BeautifulSoup
import requests
import numpy as np

url = 'https://www.carwin.ru/japanauc/see/945389787'
response = requests.get(url)
print(response)
bs = BeautifulSoup(response.text, "lxml")

temp = bs.find('div', 'content')
temp = temp.find_all('td')

FormData = [[0]*2 for i in range(len(temp)//2)]

print(FormData[1][1])

k = 0
print(range(len(temp), 2))
print(temp[0].text)
for el in range(0, len(temp), 2):

    FormData[k][0] = temp[el].text

    FormData[k][1] = temp[el+1].text
    k += 1



print(np.matrix(FormData))
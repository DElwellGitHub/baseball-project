import requests
from bs4 import BeautifulSoup

url = 'https://projects.fivethirtyeight.com/2023-mlb-predictions/games/'
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

print(soup)

print('hello there')
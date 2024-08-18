import requests
from bs4 import BeautifulSoup

url = 'https://catalog.bentley.edu/undergraduate/courses/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

coursesaz_url_list = soup.select('h2.letternav-head + ul li a')
coursesaz_url_list = ['https://catalog.bentley.edu' + url.get('href') for url in coursesaz_url_list]



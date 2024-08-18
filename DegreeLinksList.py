import requests
from bs4 import BeautifulSoup

def get_degree_url_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # url
    urls = soup.select('div.page_content ul li a') # select ul li a under the div tag page content class
    urls = ['https://catalog.bentley.edu' + url.get('href') for url in urls]
    return urls

major_url_list = get_degree_url_list('https://catalog.bentley.edu/undergraduate/programs/business-programs/')
minor_url_list = get_degree_url_list('https://catalog.bentley.edu/undergraduate/programs/minors-arts-sciences/')


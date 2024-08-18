import requests
from bs4 import BeautifulSoup
from DegreeLinksList import major_url_list, minor_url_list

def get_degree_list_dict(url_list):
    degree_url_dict = {}

    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # degree
        degree = soup.find(class_='page-title')  # find a single element with the page-title class
        degree = degree.get_text(strip=True)

        degree_url_dict[degree] = url

    return degree_url_dict

major_url_dict = get_degree_list_dict(major_url_list)
minor_url_dict = get_degree_list_dict(minor_url_list)


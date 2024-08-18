import requests
from bs4 import BeautifulSoup
from DegreeLinksList import major_url_list, minor_url_list

def get_degree_des(url_list):
    degree_des_dict = {}

    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # degree
        degree = soup.find(class_='page-title')  # find a single element with the page-title class
        degree = degree.get_text(strip=True)

        # descriptions
        descriptions = soup.find('div', id='textcontainer', class_='page_content').find_next('p')  # find the first element with the p tag, within the div tag, text contain id, and page_content class
        descriptions = descriptions.get_text(strip=True)

        degree_des_dict[degree] = descriptions

    return degree_des_dict

major_degree_des = get_degree_des(major_url_list)
minor_degree_des = get_degree_des(minor_url_list)



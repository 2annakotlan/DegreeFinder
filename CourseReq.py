import requests
import re
from bs4 import BeautifulSoup
from DegreeLinksList import major_url_list, minor_url_list

def get_degree_req(url_list):
    degree_req_dict = {}

    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # degree
        degree = soup.find(class_='page-title')  # find a single element with the page-title class
        degree = degree.get_text(strip=True)

        # classes
        if soup.find('h3', string=lambda text: text and 'Major Courses' in text):  # if it contains Major Courses
            table = (soup.find('h3', string=lambda text: text and 'Major Courses' in text)).find_next('table')
        else:
            if soup.find('h4', string='Program Requirements'):  # if it doesn't contain Major Courses but contains Program Requirements
                table = soup.find('h4', string='Program Requirements').find_next('table')
            else:  # if it doesn't contain Major Courses
                table = soup.find('table')

        rows = table.find_all('tr')  # find all rows in the table
        class_codes = [row.find('td', class_='codecol') for row in rows]  # find class code
        class_codes = [cell for cell in class_codes if cell is not None]  # filter for non-empty class-codes
        classes = [cell.find_next('td') for cell in class_codes]  # find the titles by looking at the column next to the code
        classes = [cell.get_text(strip=True) for cell in classes]
        classes = [re.sub(r'\d+$', '', word) for word in classes]  # remove any numbers at the end of the class titles

        degree_req_dict[degree] = classes

    return degree_req_dict

major_degree_req = get_degree_req(major_url_list)
minor_degree_req = get_degree_req(minor_url_list)










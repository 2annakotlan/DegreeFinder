'''
import requests
from bs4 import BeautifulSoup
import re

url = 'https://catalog.bentley.edu/undergraduate/courses/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

coursesaz_list = soup.select('h2.letternav-head + ul li a')
coursesaz_url_list = ['https://catalog.bentley.edu' + url.get('href') for url in coursesaz_list]
courseaz_department_list = [department.text.strip() for department in coursesaz_list]
courseaz_department_dict = {re.search(r"\((\w+)\)", dept).group(1): dept.split(' (')[0] for dept in courseaz_department_list}
'''

coursesaz_url_list = ['https://catalog.bentley.edu/undergraduate/courses/ac/', 'https://catalog.bentley.edu/undergraduate/courses/cdi/', 'https://catalog.bentley.edu/undergraduate/courses/mlch/', 'https://catalog.bentley.edu/undergraduate/courses/cs/', 'https://catalog.bentley.edu/undergraduate/courses/ec/', 'https://catalog.bentley.edu/undergraduate/courses/ef/', 'https://catalog.bentley.edu/undergraduate/courses/ems/', 'https://catalog.bentley.edu/undergraduate/courses/xd/', 'https://catalog.bentley.edu/undergraduate/courses/fs/', 'https://catalog.bentley.edu/undergraduate/courses/fi/', 'https://catalog.bentley.edu/undergraduate/courses/ft/', 'https://catalog.bentley.edu/undergraduate/courses/mlfr/', 'https://catalog.bentley.edu/undergraduate/courses/gls/', 'https://catalog.bentley.edu/undergraduate/courses/hi/', 'https://catalog.bentley.edu/undergraduate/courses/hnr/', 'https://catalog.bentley.edu/undergraduate/courses/id/', 'https://catalog.bentley.edu/undergraduate/courses/mlit/', 'https://catalog.bentley.edu/undergraduate/courses/la/', 'https://catalog.bentley.edu/undergraduate/courses/mg/', 'https://catalog.bentley.edu/undergraduate/courses/mk/', 'https://catalog.bentley.edu/undergraduate/courses/ma/', 'https://catalog.bentley.edu/undergraduate/courses/nasc/', 'https://catalog.bentley.edu/undergraduate/courses/ph/', 'https://catalog.bentley.edu/undergraduate/courses/prs/', 'https://catalog.bentley.edu/undergraduate/courses/psy/', 'https://catalog.bentley.edu/undergraduate/courses/sl/', 'https://catalog.bentley.edu/undergraduate/courses/so/', 'https://catalog.bentley.edu/undergraduate/courses/mlsp/', 'https://catalog.bentley.edu/undergraduate/courses/st/', 'https://catalog.bentley.edu/undergraduate/courses/ts/']
courseaz_department_dict = {'AC': 'Accounting', 'CDI': 'Career Development - Undergraduate', 'MLCH': 'Chinese', 'CS': 'Computer Information Systems', 'EC': 'Economics', 'EF': 'Economics-Finance', 'EMS': 'English & Media Studies', 'XD': 'Experience Design', 'FDS': 'Falcon Discovery Seminar', 'FI': 'Finance', 'FT': 'Finance and Technology', 'MLFR': 'French', 'GLS': 'Global Studies', 'HI': 'History', 'HNR': 'Honors Capstone Project', 'ID': 'Interdisciplinary Studies', 'MLIT': 'Italian', 'LA': 'Law', 'MG': 'Management', 'MK': 'Marketing', 'MA': 'Mathematical Sciences', 'NAS': 'Natural & Applied Sciences', 'PH': 'Philosophy', 'PRS': 'Professional Sales', 'PSY': 'Psychology', 'SL': 'Service-Learning', 'SO': 'Sociology', 'MLSP': 'Spanish', 'ST': 'Statistics', 'TS': 'Transfer Seminar'}


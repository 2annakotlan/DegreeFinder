import requests
from bs4 import BeautifulSoup
import re
from CourseAZLinks import coursesaz_url_list

def get_course_des_dict(url_list):
    course_des_dict = {}

    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        course_blocks = soup.find_all('div', class_='courseblock') # for every courseblock class...

        for block in course_blocks:
            # course
            course = block.find('p', class_='courseblocktitle noindent') # find a single p tag courseblock title noindent class element
            course = course.find(class_='') # with no subtags
            course = course.get_text(strip=True)
            course = re.sub(r'^.*\xa0', '', course) # replace '\xa0' and everything before with nothing

            # description
            description = block.find('p', class_='courseblockdesc') # find a single p tag courseblockdesc class element
            description = description.get_text(strip=True)

            course_des_dict[course] = description
    return course_des_dict

course_des = get_course_des_dict(coursesaz_url_list)



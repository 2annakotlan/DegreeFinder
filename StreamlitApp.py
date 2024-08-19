import streamlit as st
import plotly.express as px
import pandas as pd

# DISPLAY
st.title("Which Degree Best Suits You?") # title
st.sidebar.header("Select Courses") # sidebar title

# DATA
# degree requirements dictionary
major_degree_req = {'Accounting major': ['a1', 'a2', 'e3'], 'Econ major': ['e1', 'e2', 'e3'], 'Physics major': ['s1', 's2', 's3']}
minor_degree_req = {'Accounting minor': ['a1', 'a2', 'e3'], 'Econ minor': ['e6', 'e2', 'e3'], 'Math minor': ['m1', 'm2', 'm3']}
degree_req = {**major_degree_req, **minor_degree_req}

# degree descriptions dictionary
major_degree_des = {'Accounting major': "accounting description", 'Econ major': "econ description", 'Physics major':"physics description"}
minor_degree_des = {'Accounting minor': "accounting min description", 'Econ minor': "econ min description", 'Math minor':"math min description"}
degree_des = {**major_degree_des, **minor_degree_des}

# degree link dictionary
major_url_dict = {'Accounting major': "https://catalog.bentley.edu/undergraduate/programs/minors-business/accountancy-minor/", 'Econ major': "https://catalog.bentley.edu/undergraduate/programs/business-programs/business-economics/", 'Physics major':"https://catalog.bentley.edu/undergraduate/programs/arts-sciences-programs/bs-degree-programs/mathematical-sciences-major/"}
minor_url_dict = {'Accounting minor': "https://catalog.bentley.edu/undergraduate/programs/minors-business/accountancy-minor/", 'Econ minor': "https://catalog.bentley.edu/undergraduate/programs/business-programs/business-economics/", 'Math minor':"https://catalog.bentley.edu/undergraduate/programs/arts-sciences-programs/bs-degree-programs/mathematical-sciences-major/"}
url_list = {**major_url_dict, **minor_url_dict}

# all course descriptions dictionary
course_des = {'a1': 'a1 description', 'a2': 'a2 description', 'a3': 'a3 description', 'e1': 'e1 description', 'e2': 'e2 description', 'e3': 'e3 description', 'e6': 'e6 description', 'm1': 'm1 description', 'm2': 'm2 description', 'm3': 'm3 description', 'r1': 'r1 description', 's1': 's1 description', 's2': 's2 description', 's3': 's3 description'}

# filtered course descriptions dictionary for checkboxes
degree_req_courses_list = set([course for degree in degree_req.values() for course in degree]) # all unique courses in degree_req
course_des = {course: description for course, description in course_des.items() if course in degree_req_courses_list} # course_des without courses that don't exist in degree_req


# CHECKBOXES
# sidebar of checkboxes
checked_boxes = {} # dictionary to store the checked state of each checkbox

for course, course_des in course_des.items():
    checked_boxes[course] = st.sidebar.checkbox(
        label = course,  # text for the checkbox
        help = course_des  # tooltip for course description
    )

checked_courses = [course for course, checked in checked_boxes.items() if checked] # list of checked courses


# CALCULATION
# function to calculate percent degree match
def get_degree_match(degree_req):
    degree_matches_dict = {}
    degree_matches_df = pd.DataFrame(columns=['Degree','Percent Match'])

    for degree, courses in degree_req.items(): # for each degree...
        common_courses = [course for course in courses if course in checked_courses] # list of common courses between courses of interest and required courses
        num_common_courses = len(common_courses) # number of common courses between courses of interest and required courses
        num_req_courses = len(courses) # number of required courses
        if num_req_courses == 0:
            percent_degree_match = 0.0
        else:
            percent_degree_match = (num_common_courses / num_req_courses) * 100 # percent of degree completed if they were to take those courses of interest

        # save as a dictionary
        degree_matches_dict[degree] = percent_degree_match # dictionary of each degree and % match
        sorted_degree_matches_dict = dict(sorted(degree_matches_dict.items(), key=lambda item: item[1], reverse = True)) # sorted from greatest to least
        non_zero_degree_matches_dict = {degree: match for degree, match in sorted_degree_matches_dict.items() if match != 0} # removing 0 percent match

        # save as a dataframe
        degree_matches_df = degree_matches_df.append({'Degree': degree, 'Percent Match': percent_degree_match}, ignore_index = True) # dataframe of each degree and % match (not preserving the original index of the data)
        sorted_degree_matches_df = degree_matches_df.sort_values(by = 'Percent Match', ascending = False) # sorted from greatest to least
        non_zero_degree_matches_df = sorted_degree_matches_df[sorted_degree_matches_df['Percent Match'] != 0] # removing 0 percent match

    return non_zero_degree_matches_dict, non_zero_degree_matches_df

# call the function
major_degree_matches_dict, major_degree_matches_df = get_degree_match(major_degree_req)
minor_degree_matches_dict, minor_degree_matches_df = get_degree_match(minor_degree_req)

# BAR CHART
def display_bar_chart(degree_matches_df, title):
    bar_chart = px.bar(degree_matches_df,
                           x = 'Degree', # x-axis
                           y = 'Percent Match', # y-axis
                           title = title, # title
                           color = 'Percent Match',  # gradient based off of percent match column
                           color_continuous_scale = 'Blues') # blue gradient barchart

    bar_chart.update_layout(xaxis_tickangle = 90) # rotate x-axis tick labels to 90 degree
    bar_chart.update_layout(coloraxis_showscale = False) # hide color scale bar
    bar_chart.update_layout(xaxis_title = None)  # hide x-axis title
    bar_chart.update_traces(hovertemplate='%{x}: %{y:.2f}%') # hover to show degree: percentage match %
    bar_chart = st.plotly_chart(bar_chart, use_container_width = True) # display bar chart (expanding to fill the full width)
    return bar_chart

col1, col2 = st.columns(2) # creating two columns
with col1:
    display_bar_chart(major_degree_matches_df, 'Major Match')
with col2:
    display_bar_chart(minor_degree_matches_df, 'Minor Match')

# LIST
def display_list(degree_matches_dict, degree_des, url_dict):
    formatted_list = []

    for degree, percent in degree_matches_dict.items():  # for every degree...
        url = url_dict.get(degree, "No link available")  # url = get method to retrieve the urls
        tooltip = degree_des.get(degree, "No description available")  # hover = get method to retrieve the description
        formatted_list.append(f'<span style="font-size: 5px;">{percent:.2f}%: <a href="{url}" title="{tooltip}">{degree}</a></span>')

    st.markdown('<br>'.join(formatted_list), unsafe_allow_html=True)
    return formatted_list

col1, col2 = st.columns(2) # creating two columns
with col1:
    display_list(major_degree_matches_dict, major_degree_des, major_url_dict)
with col2:
    display_list(minor_degree_matches_dict, minor_degree_des, minor_url_dict)


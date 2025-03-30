from collections import defaultdict
import plotly.express as px
import streamlit as st
import pandas as pd
import re   

# DISPLAY **************************************************************************************************************
st.title("Which Degree Best Suits You?") # title
st.write("Having trouble choosing a major? Pick the classes you enjoy and discover which major best fits you!") # instructions
st.sidebar.header("Select Courses") # sidebar title

# DATA *****************************************************************************************************************
# degree requirements dictionary
from DegreeReq import major_degree_req, minor_degree_req
degree_req = {**major_degree_req, **minor_degree_req}

# degree descriptions dictionary
from DegreeDescriptions import major_degree_des, minor_degree_des

# degree link dictionary
from DegreeLinksDict import major_url_dict, minor_url_dict

# descriptions dictionary (that count towards degree requirements)
from CourseDescriptions import course_des # all course descriptions
degree_req_courses_list = set([course for degree in degree_req.values() for course in degree]) # all unique courses in degree_req
course_des = {course: description for course, description in course_des.items() if course in degree_req_courses_list} # course_des without courses that don't exist in degree_req

# a list of departments
from CourseAZLinks import courseaz_department_dict

# CHECKBOXES ***********************************************************************************************************
# initialize session state for checked boxes
if 'checked_boxes' not in st.session_state:
    st.session_state.checked_boxes = {}

# group courses by department (class code)
courses_by_department = defaultdict(list)
for course, desc in course_des.items():
    starting_letters = re.match(r"([A-Za-z\s]+)\d+", course).group(1).strip()
    courses_by_department[starting_letters].append((course, desc))

# collapsible sidebar
for dept, courses in courses_by_department.items():  # Keep the original order
    department_name = courseaz_department_dict.get(dept, dept)  # Get department name
    with st.sidebar.expander(department_name, expanded=False):
        for course, desc in courses:
            st.session_state.checked_boxes[course] = st.checkbox(
                label=f"{course} ",  # Added a space for separation
                value=st.session_state.checked_boxes.get(course, False),  # Maintain the checkbox state
                help=desc  # Tooltip for course description
            )

# list of checked courses
checked_courses = [course for course, checked in st.session_state.checked_boxes.items() if checked]  # list of checked courses

# analytics about boxes
total_selected_boxes = len(checked_courses)
total_boxes = len(course_des)
st.sidebar.markdown(f'<p style="color:#FF5733; font-weight:bold;">{total_selected_boxes} out of {total_boxes} classes selected</p>', unsafe_allow_html=True)

# CALCULATION **********************************************************************************************************
# function to calculate percent degree match
def get_degree_match(degree_req):
    degree_matches_dict = {}
    degree_matches_list = []

    for degree, courses in degree_req.items(): # for each degree...
        common_courses = [course for course in courses if course in checked_courses] # list of common courses between courses of interest and required courses
        num_common_courses = len(common_courses) # number of common courses between courses of interest and required courses
        num_req_courses = len(courses) # number of required courses
        percent_degree_match = (num_common_courses / num_req_courses) * 100 if num_req_courses != 0 else 0.0  # percent of degree completed if they were to take those courses of interest

        # save as a dictionary
        degree_matches_dict[degree] = percent_degree_match

        # prepare row for DataFrame
        degree_matches_list.append({'Degree': degree, 'Percent Match': percent_degree_match})

    # convert list of rows into a DataFrame
    degree_matches_df = pd.DataFrame(degree_matches_list)

    # sorting and filtering
    sorted_degree_matches_dict = dict(sorted(degree_matches_dict.items(), key=lambda item: item[1], reverse=True)) # sorted from greatest to least
    non_zero_degree_matches_dict = {degree: match for degree, match in sorted_degree_matches_dict.items() if match != 0} # removing 0 percent match
    sorted_degree_matches_df = degree_matches_df.sort_values(by='Percent Match', ascending=False) # sorted from greatest to least
    non_zero_degree_matches_df = sorted_degree_matches_df[sorted_degree_matches_df['Percent Match'] != 0] # removing 0 percent match

    return non_zero_degree_matches_dict, non_zero_degree_matches_df

# call the function
major_degree_matches_dict, major_degree_matches_df = get_degree_match(major_degree_req)
minor_degree_matches_dict, minor_degree_matches_df = get_degree_match(minor_degree_req)

# BAR CHART ************************************************************************************************************
def display_bar_chart(degree_matches_df, title):
    degree_matches_df = degree_matches_df.head(10) # only display the first 10 matches for visual aesthetics
    bar_chart = px.bar(degree_matches_df,
                           x = 'Degree', # x-axis
                           y = 'Percent Match', # y-axis
                           title = title, # title
                           color = 'Percent Match',  # gradient based off of percent match column
                           color_continuous_scale = 'Blues') # blue gradient barchart
    bar_chart.update_layout(xaxis_title=None) # hide x-axis label "degree"
    bar_chart.update_layout(coloraxis_showscale = False) # hide color scale bar
    bar_chart.update_layout(xaxis_tickangle=90)  # make the x-axis labels verticle
    bar_chart.update_traces(hovertemplate='%{x}: %{y:.2f}%') # hover to show degree: percentage match %
    bar_chart = st.plotly_chart(bar_chart, use_container_width = True) # display bar chart (expanding to fill the full width)
    return bar_chart

col1, col2 = st.columns(2) # creating two columns
with col1:
    if not major_degree_matches_df.empty: # don't have an empty graph
        display_bar_chart(major_degree_matches_df, 'Major Match')
with col2:
    if not minor_degree_matches_df.empty: # don't have an empty graph
        display_bar_chart(minor_degree_matches_df, 'Minor Match')

# LIST *****************************************************************************************************************
def display_list(degree_matches_dict, degree_des, url_dict):
    formatted_list = []

    for degree, percent in degree_matches_dict.items():  # for every degree...
        url = url_dict.get(degree, "No link available")  # url = get method to retrieve the urls
        tooltip = degree_des.get(degree, "No description available")  # hover = get method to retrieve the description
        formatted_list.append(f'<span style="font-size: 12px;">{percent:.2f}%: <a href="{url}" title="{tooltip}">{degree}</a></span>')

    st.markdown('<br>'.join(formatted_list), unsafe_allow_html=True)
    return formatted_list

col1, col2 = st.columns(2) # creating two columns
with col1:
    display_list(major_degree_matches_dict, major_degree_des, major_url_dict)
with col2:
    display_list(minor_degree_matches_dict, minor_degree_des, minor_url_dict)
    
# GOOGLE SHEETS ********************************************************************************************************
from GoogleSheets import *

if st.button("Submit Results"):
    #update_columns(sheet_name = "MajorPredictions", sheet_id = 0) # uncomment this out when new degrees are offered
    st.success("DONE")

# DISPLAY **************************************************************************************************************
st.markdown('<p style="font-weight:bold;">Designed by Anna Kotlan, Class of 2025</p>', unsafe_allow_html=True)

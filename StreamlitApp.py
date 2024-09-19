import streamlit as st
import pandas as pd
import plotly.express as px

# DISPLAY **************************************************************************************************************
st.title("Which Degree Best Suits You?") # title
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

# department dictionary (that count towards degree requirements)
from CourseDepartment import course_department # all course departments

# Filtering only once for degree_req courses
degree_req_courses_list = {course for courses in degree_req.values() for course in courses}
course_des = {course: description for course, description in course_des.items() if course in degree_req_courses_list}
course_department = {course: department for course, department in course_department.items() if course in degree_req_courses_list}

# DROPDOWNS AND FILTERS ************************************************************************************************
displayed_course_des = course_des.copy() # displayed courses

# main dropdown
selected_filter_type = st.sidebar.selectbox(label="Filter by...", options=[" ", "department", "degree", "class"], index=0)

# Filter courses based on the selected filter type
if selected_filter_type == "department":
    selected_departments = st.sidebar.multiselect(label="Select department(s)...", options=list(set(course_department.values())), default=[])
    if selected_departments:
        displayed_course_des = {course: description for course, dept in course_department.items() if dept in selected_departments}
elif selected_filter_type == "degree":
    selected_degrees = st.sidebar.multiselect(label="Select degree(s)...", options=list(degree_req.keys()), default=[])
    if selected_degrees:
        displayed_course_des = {course: description for course in set(course for degree in selected_degrees for course in degree_req[degree]) if course in course_des}
elif selected_filter_type == "class":
    search_query = st.sidebar.text_input(label="Search for a class...", value="")
    if search_query:
        displayed_course_des = {course: description for course, description in course_des.items() if search_query.lower() in course.lower()}

# CHECKBOXES ***********************************************************************************************************
# Initialize session state only for displayed courses
if 'checked_boxes' not in st.session_state:
    st.session_state.checked_boxes = {course: False for course in displayed_course_des}

# Update session state only for displayed courses
for course in displayed_course_des:
    st.session_state.checked_boxes[course] = st.sidebar.checkbox(
        label=course, 
        help=displayed_course_des[course], 
        value=st.session_state.checked_boxes.get(course, False)
    )

checked_courses = [course for course, checked in st.session_state.checked_boxes.items() if checked] # List of checked courses

# Analytics about boxes
total_selected_boxes = len(checked_courses)
total_boxes = len(course_des)
st.sidebar.markdown(f'<p style="color:#FF5733; font-weight:bold;">{total_selected_boxes} out of {total_boxes} classes selected</p>', unsafe_allow_html=True)

# CALCULATION **********************************************************************************************************
# Function to calculate percent degree match
def get_degree_match(degree_req, checked_courses):
    degree_matches = [
        {
            'Degree': degree,
            'Percent Match': (len([course for course in courses if course in checked_courses]) / len(courses)) * 100 if len(courses) > 0 else 0.0
        }
        for degree, courses in degree_req.items()
    ]
    return pd.DataFrame(degree_matches).sort_values(by='Percent Match', ascending=False)

# Call the function
major_degree_matches_df = get_degree_match(major_degree_req, checked_courses)
minor_degree_matches_df = get_degree_match(minor_degree_req, checked_courses)

# BAR CHART ************************************************************************************************************
def display_bar_chart(degree_matches_df, title):
    degree_matches_df = degree_matches_df.head(10)  # Limit to top 10 matches
    bar_chart = px.bar(degree_matches_df, x='Degree', y='Percent Match', title=title, color='Percent Match', color_continuous_scale='Blues')
    bar_chart.update_layout(xaxis_title=None, coloraxis_showscale=False, xaxis_tickangle=90)
    bar_chart.update_traces(hovertemplate='%{x}: %{y:.2f}%')
    st.plotly_chart(bar_chart, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    if not major_degree_matches_df.empty:
        display_bar_chart(major_degree_matches_df, 'Major Match')
with col2:
    if not minor_degree_matches_df.empty:
        display_bar_chart(minor_degree_matches_df, 'Minor Match')

# LIST *****************************************************************************************************************
def display_list(degree_matches_df, degree_des, url_dict):
    formatted_list = [
        f'<span style="font-size: 12px;">{percent:.2f}%: <a href="{url_dict.get(degree, "No link available")}" title="{degree_des.get(degree, "No description available")}">{degree}</a></span>'
        for degree, percent in zip(degree_matches_df['Degree'], degree_matches_df['Percent Match'])
    ]
    st.markdown('<br>'.join(formatted_list), unsafe_allow_html=True)

with col1:
    display_list(major_degree_matches_df, major_degree_des, major_url_dict)
with col2:
    display_list(minor_degree_matches_df, minor_degree_des, minor_url_dict)

# FOOTER ***************************************************************************************************************
st.markdown('<p style="font-weight:bold;">Designed by Anna Kotlan, Class of 2025</p>', unsafe_allow_html=True)

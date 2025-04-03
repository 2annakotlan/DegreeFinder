from collections import defaultdict
import plotly.express as px  
import streamlit as st
import pandas as pd 
import re    

# DATA *****************************************************************************************************************
# google sheets functions
from GoogleSheets import update_prediction_columns, append_prediction_data, append_student_data, get_average_scores   

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

# DISPLAY LOGIN PAGE ***************************************************************************************************
def display_login_page():
    st.title("Degree Finder") # title 
    st.header("Log In") # login
    
    with st.form(key='login_form'):
        id = st.text_input("Student ID:") # login
        major = st.multiselect("Major (if declared):", list(major_url_dict.keys()), max_selections=2) # major
        minor = st.multiselect("Minor (if declared):", list(minor_url_dict.keys()), max_selections=2) # minor
        major_1, major_2 = (major + [""] * 2)[:2] # assigning major, defaulting to empty string if nothing selected
        minor_1, minor_2 = (minor + [""] * 2)[:2] # assigning minor, defaulting to empty string if nothing selected
        submitted = st.form_submit_button("Next") # submit
    
    if submitted and not id:
        st.error("Student ID Required") # error message 

    if submitted and id:
        st.session_state["id"] = id # save in state session
        st.session_state["major_1"] = major_1 # save in state session
        st.session_state["major_2"] = major_2 # save in state session
        st.session_state["minor_1"] = minor_1 # save in state session
        st.session_state["minor_2"] = minor_2 # save in state session
        
        st.session_state.page = 'display_analytics_page'
        st.rerun()

# DISPLAY ANALYTICS PAGE ***********************************************************************************************
def display_analytics_page():
    st.title(f"Degree Finder") # title    
    st.sidebar.header("Select Courses")  # sidebar title
    st.write("Having trouble choosing a major? Pick the classes you enjoy and discover which major best fits you!") # instructions
    
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
    for dept, courses in courses_by_department.items():  # keep the original order
        department_name = courseaz_department_dict.get(dept, dept)  # get department name
        with st.sidebar.expander(department_name, expanded=False):
            for course, desc in courses:
                st.session_state.checked_boxes[course] = st.checkbox(
                    label=f"{course} ",  # added a space for separation
                    value=st.session_state.checked_boxes.get(course, False),  # maintain the checkbox state
                    help=desc)  # tooltip for course description
    
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
    def display_bar_chart(degree_matches_df, title, accuracy):
        degree_matches_df = degree_matches_df.head(10) # only display the first 10 matches for visual aesthetics
        bar_chart = px.bar(degree_matches_df,
                               x = 'Degree', # x-axis
                               y = 'Percent Match', # y-axis
                               # title = title, # title
                               color = 'Percent Match',  # gradient based off of percent match column
                               color_continuous_scale = 'Blues') # blue gradient barchart
        bar_chart.update_layout(xaxis_title=None) # hide x-axis label "degree"
        bar_chart.update_layout(coloraxis_showscale = False) # hide color scale bar
        bar_chart.update_layout(xaxis_tickangle=90)  # make the x-axis labels verticle
        bar_chart.update_traces(hovertemplate='%{x}: %{y:.2f}%') # hover to show degree: percentage match %
        st.markdown(f'<p style="font-weight:bold;" title="{accuracy}% Accuracy">{title}</p>', unsafe_allow_html=True)
        bar_chart = st.plotly_chart(bar_chart, use_container_width = True) # display bar chart (expanding to fill the full width)
        return bar_chart
    
    major_accuracy_average, minor_accuracy_average = get_average_scores() # accuracy scores
    
    col1, col2 = st.columns(2) # creating two columns
    with col1:
        if not major_degree_matches_df.empty: # don't have an empty graph
            display_bar_chart(major_degree_matches_df, 'Major Match', major_accuracy_average)
    with col2:
        if not minor_degree_matches_df.empty: # don't have an empty graph
            display_bar_chart(minor_degree_matches_df, 'Minor Match', minor_accuracy_average)
    
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
    if len(major_degree_matches_dict) >= 1 or len(minor_degree_matches_dict) >= 1:
        if st.button("Submit Results"):

            # retrieve stored information 
            id = st.session_state.get("id") 
            major_1 = st.session_state.get("major_1") 
            major_2 = st.session_state.get("major_2") 
            minor_1 = st.session_state.get("minor_1") 
            minor_2 = st.session_state.get("minor_2") 

            # scaling factor
            major_scale = 1/(max(major_degree_matches_dict.values()))
            minor_scale = 1/(max(minor_degree_matches_dict.values()))
            
            # retrieve scores (if degree not listed, return 0; if degree not inputted, N/A) 
            major_1_raw_score = (major_degree_matches_dict.get(major_1, 0) if major_1 else "")
            major_2_raw_score = (major_degree_matches_dict.get(major_2, 0) if major_2 else "") 
            minor_1_raw_score = (minor_degree_matches_dict.get(minor_1, 0) if minor_1 else "") 
            minor_2_raw_score = (minor_degree_matches_dict.get(minor_2, 0) if minor_2 else "") 

            # scaling scores
            major_1_scaled_score = major_1_raw_score * major_scale if isinstance(major_1_raw_score, (int, float)) else major_1_raw_score
            major_2_scaled_score = major_2_raw_score * major_scale if isinstance(major_2_raw_score, (int, float)) else major_2_raw_score
            minor_1_scaled_score = minor_1_raw_score * minor_scale if isinstance(minor_1_raw_score, (int, float)) else minor_1_raw_score
            minor_2_scaled_score = minor_2_raw_score * minor_scale if isinstance(minor_2_raw_score, (int, float)) else minor_2_raw_score

            # update prediction spreadsheet with new degree offerings 
            #update_prediction_columns(sheet_name = "MajorPredictions", sheet_id = 0) 
            #update_prediction_columns(sheet_name = "MinorPredictions", sheet_id = 375147427) 
            
            # update prediction spreadsheet with results
            append_prediction_data(data = major_degree_matches_dict, id = id, sheet_name = "MajorPredictions") 
            append_prediction_data(data = minor_degree_matches_dict, id = id, sheet_name = "MinorPredictions") 

            # update student data spreadsheet with results
            append_student_data(id, major_1, major_2, minor_1, minor_2, major_1_scaled_score, major_2_scaled_score, minor_1_scaled_score, minor_2_scaled_score)   
            
            st.success("Submitted") 

    # DISPLAY **************************************************************************************************************
    st.markdown('<p style="font-weight:bold;">Designed by Anna Kotlan, Class of 2025</p>', unsafe_allow_html=True)

# PAGE ROUTING *********************************************************************************************************
if 'page' not in st.session_state:
    st.session_state.page = 'display_login_page'
if st.session_state.page == 'display_login_page':
    display_login_page()
if st.session_state.page == 'display_analytics_page':
    display_analytics_page()

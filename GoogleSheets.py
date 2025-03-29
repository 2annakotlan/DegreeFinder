import streamlit as st
from googleapiclient.discovery import build 
from google.oauth2.service_account import Credentials 
from DegreeLinksDict import major_url_dict, minor_url_dict

spreadsheetId = '16xVJWtgcHnHUFU9kbQ8N_QHb4mXX57KiN3WyDooApTY'
service = build('sheets', 'v4', credentials=Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets']))


def add_column(sheet_name):
    #values = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!1:1").execute()).get('values', []) # first row
    spreadsheet_degrees = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1').execute().get('values', []))[0]
    st.write(spreadsheet_degrees)
    #next_row = len(values) + 1 # next row number
    #st.write(next_row)
    #service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"{sheet_name}!A{next_row}:A", valueInputOption="RAW", body={"values": [['Test']]}, ).execute() # update next column

'''
def add_columns(sheet_name):
    spreadsheet_degrees = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1').execute().get('values', []))[0] # current spreadsheet degrees (columns), flattened
    webscraped_degrees = list(major_url_dict.keys()) # current webscraped degrees
    new_degrees = [degree for degree in webscraped_degrees if degree not in spreadsheet_degrees] # degrees in webscraped degrees not included in spreadsheet degrees
    service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"{sheet_name}!1:1", valueInputOption="RAW", body={"values": [['Test']]}).execute() # adding new degrees as columns
'''

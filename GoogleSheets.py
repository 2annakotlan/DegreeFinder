import streamlit as st
from googleapiclient.discovery import build 
from google.oauth2.service_account import Credentials 
from DegreeLinksDict import major_url_dict, minor_url_dict   

spreadsheetId = '16xVJWtgcHnHUFU9kbQ8N_QHb4mXX57KiN3WyDooApTY'
service = build('sheets', 'v4', credentials=Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets']))

# UPDATE SPREADSHEET WITH NEW DEGREE OFFERINGS *************************************************************************
def update_columns(sheet_name, sheet_id): 
    # Finding New Degrees 
    spreadsheet_degrees = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1').execute().get('values', []))[0] # current spreadsheet degrees 
    webscraped_degrees = list(major_url_dict.keys()) # current webscraped degrees
    new_degrees = [degree for degree in webscraped_degrees if degree not in spreadsheet_degrees] # unique webscraped degrees 

    # Adding New Degrees to Column Headers
    if len(new_degrees) > 0: # if there are new degrees that need to be added...
        num_column_needed = len(spreadsheet_degrees) + len(new_degrees) # number of columns needed
        letter_column_needed = chr(64 + num_column_needed) if num_column_needed <= 26 else chr(64 + (num_column_needed - 1) // 26) + chr(65 + (num_column_needed - 1) % 26) # letter equivalent of next_column_number
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={"requests": [{"updateSheetProperties": {"properties": {"sheetId": sheet_id, "gridProperties": {"columnCount": num_column_needed}}, "fields": "gridProperties.columnCount"}}]}).execute() # insert empty column(s)
        service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=f"{sheet_name}!{letter_column_needed}1", valueInputOption="RAW", body={"values": [new_degrees]}).execute() # fill in new column

# UPDATE SPREADSHEET WITH RESUlts **************************************************************************************
def append_data(data, sheet_name):
    spreadsheet_degrees = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1').execute().get('values', []))[0] # spreadsheet columns
    values = [data.get(degree, '') for degree in spreadsheet_degrees] # create row to append, matching dictionary keys to headers
    service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=sheet_name, valueInputOption="RAW", body={"values": [values]}).execute() # fill in row

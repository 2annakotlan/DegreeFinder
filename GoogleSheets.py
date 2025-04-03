import streamlit as st
from datetime import datetime
from googleapiclient.discovery import build 
from google.oauth2.service_account import Credentials 

spreadsheetId = '16xVJWtgcHnHUFU9kbQ8N_QHb4mXX57KiN3WyDooApTY'
service = build('sheets', 'v4', credentials=Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets']))

# UPDATE SPREADSHEET WITH NEW DEGREE OFFERINGS *************************************************************************
def update_prediction_columns(sheet_name, sheet_id): 
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

# UPDATE SPREADSHEET WITH PREDICTION RESUltS ***************************************************************************
def append_prediction_data(data, id, sheet_name):
    id_column = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!A2:A').execute().get('values', [])
    row_number = next((row_number for row_number, row in enumerate(id_column, start=2) if row and row[0] == id), None) # find row number where id already exists

    spreadsheet_degrees = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1').execute().get('values', []))[0] # spreadsheet columns
    values = [data.get(degree, 0) for degree in spreadsheet_degrees] # create row to append - in correct position, matching dictionary keys to headers
    values[spreadsheet_degrees.index('Student ID')] = id  # put id in correct position
    values[spreadsheet_degrees.index('Timestamp')] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # set current timestamp in correct position

    if row_number == None: 
        service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=f"{sheet_name}", valueInputOption="RAW", body={"values": [values]}).execute() # append data in next row
    else: 
        service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"{sheet_name}!{row_number}:{row_number}", valueInputOption="RAW", body={"values": [values]}).execute() # replace data in specified row

# UPDATE SPREADSHEET WITH STUDENT DATA *********************************************************************************
def append_student_data(id, major_1, major_2, minor_1, minor_2):
    id_column = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='StudentInfo!A2:A').execute().get('values', [])
    row_number = next((row_number for row_number, row in enumerate(id_column, start=2) if row and row[0] == id), None) # find row number where id already exists
    
    spreadsheet_columns = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range="StudentInfo!1:1").execute().get('values', []))[0] # spreadsheet columns
    values = [''] * len(spreadsheet_columns) # placeholder to be replaced with data
    values[spreadsheet_columns.index('Student ID')] = id  # put id in correct position
    values[spreadsheet_columns.index('Major 1')] = major_1  # put major 1 in correct position
    values[spreadsheet_columns.index('Major 2')] = major_2  # put major 2 in correct position
    values[spreadsheet_columns.index('Minor 1')] = minor_1  # put minor 1 in correct position
    values[spreadsheet_columns.index('Minor 2')] = minor_2  # put minor 2 in correct position 

    if row_number == None: 
        service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range="StudentInfo", valueInputOption="RAW", body={"values": [values]}).execute() # append data in next row
    else: 
        service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"StudentInfo!{row_number}:{row_number}", valueInputOption="RAW", body={"values": [values]}).execute() # replace data in specified row

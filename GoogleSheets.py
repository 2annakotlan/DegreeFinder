import streamlit as st
from googleapiclient.discovery import build 
from google.oauth2.service_account import Credentials 
from DegreeLinksDict import major_url_dict, minor_url_dict

spreadsheetId = '16xVJWtgcHnHUFU9kbQ8N_QHb4mXX57KiN3WyDooApTY'
service = build('sheets', 'v4', credentials=Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets']))

def add_column(sheet_name): 
    #values = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!1:1").execute()).get('values', []) 
    #next_column_number = len(values[0]) + 1
    #next_column_letter = chr(64 + next_column_number) if next_column_number <= 26 else chr(64 + (next_column_number - 1) // 26) + chr(65 + (next_column_number - 1) % 26)
    #requests = [{"updateSheetProperties": {"properties": {"sheetId": 0}, "fields": "gridProperties.columnCount", "gridProperties": {"columnCount": next_column_number}}}]
    
    requests = [{"updateSheetProperties": {"properties": {"sheetId": 0}, "fields": "gridProperties.columnCount", "gridProperties": {"columnCount": 37}}}]
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={"requests": requests}).execute()
    #service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"{sheet_name}!{next_column_letter}1:{next_column_letter}", valueInputOption="RAW", body={"values": [['New Column']]}).execute()

'''
def add_columns(sheet_name):
    spreadsheet_degrees = (service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1').execute().get('values', []))[0] # current spreadsheet degrees (columns), flattened
    webscraped_degrees = list(major_url_dict.keys()) # current webscraped degrees
    new_degrees = [degree for degree in webscraped_degrees if degree not in spreadsheet_degrees] # degrees in webscraped degrees not included in spreadsheet degrees
    service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"{sheet_name}!1:1", valueInputOption="RAW", body={"values": [['Test']]}).execute() # adding new degrees as columns
'''

import streamlit as st
import pandas as pd
from googleapiclient.discovery import build 
from google.oauth2.service_account import Credentials

spreadsheetId = '16xVJWtgcHnHUFU9kbQ8N_QHb4mXX57KiN3WyDooApTY'

def get_sheets_service():
    credentials = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets'])
    return build('sheets', 'v4', credentials=credentials)

service = get_sheets_service()

def read_values(sheet_name, column_name, row_name):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=sheet_name).execute()
    data = result.get('values', [])
    if not data: 
        return pd.DataFrame()
    df = pd.DataFrame(data[1:], columns=data[0])
    if row_name is None and column_name is not None:
        values = df[[column_name]]  
    elif column_name is None and row_name is not None:
        values = df[df.iloc[:, 0] == row_name] 
    elif row_name is not None and column_name is not None:
        values = df[df.iloc[:, 0] == row_name][[column_name]] 
    return values 
    
def edit_values(sheet_name, column_name, row_name, value):
    column_names = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!1:1").execute().get("values", [[]])[0]
    column_index = chr(65 + column_names.index(column_name))
    row_names = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!A:A").execute().get("values", [[]])
    row_index = len(row_names) + 1 if row_name == "append" else [row[0] for row in row_names].index(row_name) + 1
    service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"{sheet_name}!{column_index}{row_index}", valueInputOption="RAW", body={"values": [[value]]}).execute()

def insert_row(sheet_name, values):
    next_row = len(service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!A:A").execute().get("values", [])) + 1
    service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"{sheet_name}!A{next_row}", valueInputOption="RAW", body={"values": [values]}).execute()

def delete_row(sheet_name, row_name):
    row_values = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!A:A").execute().get("values", [[]])
    row_index = next(i for i, row in enumerate(row_values, start=1) if row and row[0] == row_name)
    sheet_id = next(sheet["properties"]["sheetId"] for sheet in service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()["sheets"] if sheet["properties"]["title"] == sheet_name)
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={"requests": [{"deleteDimension": {"range": {"sheetId": sheet_id, "dimension": "ROWS", "startIndex": row_index - 1, "endIndex": row_index}}}]}).execute()

def create_sheet(sheet_name):
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={'requests': [{"addSheet": {"properties": {"title": sheet_name}}}]}).execute()

def delete_sheet(sheet_name):
    spreadsheets = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheets = spreadsheets.get('sheets', [])
    sheet_id = next((sheet["properties"]["sheetId"] for sheet in sheets if sheet["properties"]["title"] == sheet_name), None)
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={'requests': [{"deleteSheet": {"sheetId": sheet_id}}]}).execute()

def read_sheet():
    spreadsheets = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheets = spreadsheets.get('sheets', [])
    sheet_names = [sheet["properties"]["title"] for sheet in sheets]
    return sheet_names

def read_column(sheet_name):
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=sheet_name).execute()
    data = result.get('values', [])
    df = pd.DataFrame(data[1:], columns=data[0])  
    header = df.columns  
    return header

def add_column(sheet_name, value):
    column_names = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!1:1").execute().get('values', [[]])[0]  
    column_index = chr(64 + len(column_names) + 1 )  
    service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f"{sheet_name}!{column_index}1", valueInputOption="RAW", body={"values": [[value]]}).execute()

def delete_column(sheet_name, column_name):
    column_index = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!1:1").execute().get('values', [[]])[0].index(column_name)
    sheet_id = next(sheet['properties']['sheetId'] for sheet in service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()['sheets'] if sheet['properties']['title'] == sheet_name)
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={'requests': [{"deleteDimension": {"range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": column_index, "endIndex": column_index + 1}}}]}).execute()


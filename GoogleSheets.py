import streamlit as st
from googleapiclient.discovery import build 
from google.oauth2.service_account import Credentials 

spreadsheetId = '16xVJWtgcHnHUFU9kbQ8N_QHb4mXX57KiN3WyDooApTY'
service = build('sheets', 'v4', credentials=Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets']))

def get_existing_columns():
    sheet_name = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()['sheets'][0]['properties']['title']
    return service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1').execute().get('values', [[]])[0]

def update_columns(major_url_dict):
    sheet_name = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()['sheets'][0]['properties']['title']
    existing_cols = set(get_existing_columns())
    new_cols = sorted(existing_cols | (set(major_url_dict.keys()) - existing_cols))
    service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1', valueInputOption='RAW', body={'values': [new_cols]}).execute()

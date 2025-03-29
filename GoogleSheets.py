import streamlit as st
import pandas as pd
from googleapiclient.discovery import build 
from google.oauth2.service_account import Credentials 

spreadsheetId = '16xVJWtgcHnHUFU9kbQ8N_QHb4mXX57KiN3WyDooApTY'

def get_sheets_service():
    credentials = Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets'])
    return build('sheets', 'v4', credentials=credentials)

service = get_sheets_service()

def append_row_by_headers(data, sheet_name="Sheet1"):
    column_headers = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f"{sheet_name}!1:1").execute().get('values', [])[0]
    values = [data.get(header, "") for header in column_headers]
    service.spreadsheets().values().append(spreadsheetId=spreadsheetId, range=sheet_name, valueInputOption="RAW", body={"values": [values]}).execute()


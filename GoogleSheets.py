import streamlit as st
from googleapiclient.discovery import build 
from google.oauth2.service_account import Credentials 

spreadsheetId = '16xVJWtgcHnHUFU9kbQ8N_QHb4mXX57KiN3WyDooApTY'
service = build('sheets', 'v4', credentials=Credentials.from_service_account_info(st.secrets["google_service_account"], scopes=['https://www.googleapis.com/auth/spreadsheets']))

def get_columns(sheet_name):
    values = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=f'{sheet_name}!1:1').execute().get('values', [])
    return (values)


    

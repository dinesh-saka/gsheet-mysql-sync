from googleapiclient.discovery import build
from .sheets_api import authenticate_google_sheets

def read_sheet_data(spreadsheet_id, range_name):
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])

def write_sheet_data(spreadsheet_id, range_name, values):
    creds = authenticate_google_sheets()
    service = build('sheets', 'v4', credentials=creds)
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    return result

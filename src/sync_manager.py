import time
from src.mysql.mysql_sync import sync_google_sheet_to_mysql, sync_mysql_to_google_sheet

def real_time_sync(spreadsheet_id, range_name, table_name):
    while True:
        sync_google_sheet_to_mysql(spreadsheet_id, range_name, table_name)
        sync_mysql_to_google_sheet(spreadsheet_id, range_name, table_name)
        time.sleep(5)  # Adjust this duration based on your requirements

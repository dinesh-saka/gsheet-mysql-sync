from src.sync_manager import real_time_sync

SPREADSHEET_ID = ''
RANGE_NAME = ''
TABLE_NAME = ''

if __name__ == "__main__":
    real_time_sync(SPREADSHEET_ID, RANGE_NAME, TABLE_NAME)

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_google_sheets():
    creds = None
    # Load credentials if they exist
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If no valid credentials are available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',
                    scopes=SCOPES  # No need for redirect_uri here
                )
            creds = flow.run_local_server(port=51796)  # Use a fixed port here
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


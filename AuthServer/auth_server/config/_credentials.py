
import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def _load_credential_from_file(filepath):
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, "rb") as f:
        return f.read()

def _load_google_gmail_api_credentials_from_file(filepath):
    credentials_path = os.path.join(os.path.dirname(__file__), filepath)
    
    scopes = [
    "https://www.googleapis.com/auth/gmail.send"
    ]

    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, scopes=scopes
    )
    
    creds = flow.run_local_server(port=0)
    
    return creds

def _load_google_drive_api_credentials_from_file(filepath):
    credentials_path = os.path.join(os.path.dirname(__file__), filepath)
    
    scopes = [
    "https://www.googleapis.com/auth/drive"
    ]

    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, scopes=scopes
    )
    
    creds = flow.run_local_server(port=0)
    
    return creds

SERVER_CERTIFICATE = _load_credential_from_file("credentials\\localhost.crt")
SERVER_CERTIFICATE_KEY = _load_credential_from_file("credentials\\localhost.key")
ROOT_CERTIFICATE = _load_credential_from_file("credentials\\root.crt")
GMAIL_API_CREDENTIALS = _load_google_gmail_api_credentials_from_file("credentials\\client_secret.json")
DRIVE_API_CREDENTIALS = _load_google_drive_api_credentials_from_file("credentials\\client_secret.json")
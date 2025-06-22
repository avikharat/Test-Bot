# youtube_service_auth.py

import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()  # Load from .env file

def get_youtube_service_from_env():
    creds = Credentials(
        token=None,
        refresh_token=os.getenv("YT_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("YT_CLIENT_ID"),
        client_secret=os.getenv("YT_CLIENT_SECRET"),
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)

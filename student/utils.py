# student/utils.py
from .models import Milestone
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

DEFAULT_TITLES = [
    "Chapter 1: Introduction",
    "Chapter 2: Literature Review",
    "Chapter 3: Methodology",
    "Chapter 4: Results",
    "Chapter 5: Discussion",
    "Full Report Submission"
]

def create_default_milestones(student):
    for title in DEFAULT_TITLES:
        Milestone.objects.get_or_create(student=student, title=title)



def get_drive_service():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials', 'google-drive-access-key.json')

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)
    return service


def list_library_files(folder_id):
    service = get_drive_service()
    results = service.files().list(
        q=f"'{folder_id}' in parents and trashed = false",
        fields="files(id, name, webViewLink, createdTime)"
    ).execute()
    return results.get('files', [])

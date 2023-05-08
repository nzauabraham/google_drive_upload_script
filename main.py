import io
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

# Replace the values below with your own values
SERVICE_ACCOUNT_FILE = '/path/to/service/account/file.json'
FILE_PATH = 'test.txt'
FOLDER_ID = '1234abcdefg'  # Folder ID from Google Drive

# Authenticate with Google Drive API using service account credentials
creds = None
try:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive'])
except Exception as e:
    print(f'Error authenticating with Google Drive API: {e}')
    exit()

# Create Google Drive API client
drive_service = build('drive', 'v3', credentials=creds)

# Create file metadata
file_metadata = {'name': os.path.basename(FILE_PATH)}
if FOLDER_ID:
    file_metadata['parents'] = [FOLDER_ID]

# Create file media object
media = MediaIoBaseUpload(io.FileIO(FILE_PATH, 'rb'), mimetype='application/octet-stream', chunksize=1024 * 1024)

# Upload the file to Google Drive
file = None
try:
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id').execute()
    print(f'File ID: {file.get("id")}')
except HttpError as error:
    print(f'An error occurred: {error}')
    file = None

if file is None:
    print('Error uploading file to Google Drive')
else:
    print('File uploaded successfully to Google Drive')

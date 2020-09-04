from datetime import datetime, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import os

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def upload():
	creds = service_account.Credentials.from_service_account_file(os.environ['SERVICE_ACCOUNT_FILE'], scopes=SCOPES)
	drive_service = build('drive', 'v3', credentials=creds)
	folder_meta = {
		'name': datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M"),
		'mimeType': 'application/vnd.google-apps.folder',
		'parents': [os.environ['ROOT_FOLDER_ID']],
	}
	folder = drive_service.files().create(body=folder_meta, fields='id').execute()
	folder_id = folder.get('id')
	dump_dir = os.environ['DUMP_DIR']
	backup_file_names = os.listdir(dump_dir)
	for f in backup_file_names:
		file_metadata = {
			'name': f,
			'parents': [folder_id],
		}
		abs_file_name = os.path(dump_dir, f)
		media = MediaFileUpload(abs_file_name)
		drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
	

if __name__ == '__main__':
	upload()

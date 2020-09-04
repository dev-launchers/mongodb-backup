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
	root_dir_id = create_folder(drive_service, datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M"), os.environ['ROOT_FOLDER_ID'])
	
	# DUMP_DIR needs to be absolute path
	dump_dir = os.environ['DUMP_DIR']
	created_dir = {dump_dir: root_dir_id}
	print("dump dir {}".format(dump_dir))
	print("root dir {}".format(root_dir_id))
	
	for (parent_dir, dirnames, fnames) in os.walk(dump_dir):
		print("parent {}, dirs {}, files {}".format(parent_dir, dirnames, fnames))
		parent_id = created_dir[parent_dir]
		for dirname in dirnames:
			dir_id = create_folder(drive_service, dirname, parent_id)
			abs_dir_path = os.path.join(parent_dir, dirname)
			created_dir[abs_dir_path] = dir_id			

		for fname in fnames:
			abs_file_path = os.path.join(parent_dir, fname)
			upload_file(drive_service, fname, abs_file_path, parent_id)
	
def create_folder(drive_service, name, parent_id):
	folder_meta = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id],
        }
	folder = drive_service.files().create(body=folder_meta, fields='id').execute()
	return folder.get('id')

def upload_file(drive_service, name, abs_path, folder_id):
	file_metadata = {
		'name': name,
		'parents': [folder_id],
	}
	media = MediaFileUpload(abs_path)
	drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute() 

if __name__ == '__main__':
	upload()

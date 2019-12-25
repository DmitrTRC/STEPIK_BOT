from google.cloud import storage
from google.oauth2 import service_account
import json
import os
try:

    credentials_raw = os.environ.get('HDRIVE_GOOGLE_JSON_KEY')
    service_account_info = json.loads(credentials_raw)
    project = service_account_info.get('project_id')
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
except Exception as er:
    print(f'Error to get Google Key access : {er=}')
else:
    print(f'Google access granted! {credentials=}')

try:
    drive_client = storage.Client(credentials=credentials, project=project)

except Exception as er:
    print(f'Error to get Google Key access : {er=}')
else:
    print(f'Google access granted! {drive_client=}')

try:
    bucket = 'dmheroku'
    bucket_handler = drive_client.get_bucket(bucket)

except  Exception as er:
    print(f'Goggle storage error : {er=} ')

from aws import get_secret, set_secret
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import time
from datetime import datetime as dt
import pandas as pd

from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO, StringIO

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']


def get_service(project_id, credential_id):
    secret_key = f'mini-hub/{project_id}'
    secret = get_secret(secret_key, credential_id)
    creds = None

    if 'token' in secret.keys():
        creds = Credentials.from_authorized_user_info(secret['token'], SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_config(
                secret['client_secret'], SCOPES,
                redirect_uri='http://localhost')

            auth_url, _ = flow.authorization_url(prompt='consent')
            print('Please go to this URL: {}'.format(auth_url))
            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)
            creds = flow.credentials

        secret['token'] = json.loads(creds.to_json())
        set_secret(secret_key, credential_id, secret)

    try:
        service = build('drive', 'v3', credentials=creds)
        return service

    except HttpError as error:
        print(f'An error occurred: {error}')


def get_new_files(service, folder_id, last_update, dt_format='%Y-%m-%dT%H:%M:%S.%fZ'):
    page_token = None
    newfiles = []
    while True:
        response = service.files().list(q=f"'{folder_id}' in parents",
                                        spaces='drive',
                                        fields='*',
                                        pageToken=page_token).execute()
        for file in response['files']:
            created_time = dt.strptime(file['createdTime'], dt_format)
            if created_time > last_update:
                newfiles.append(file['id'])
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return newfiles


def get_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    file = BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    time.sleep(5)
    return file.getvalue()


if __name__ == '__main__':
    project_name = 'project_bat'
    credential_id = 'google_drive_credential'

    svc = get_service(project_name, credential_id)

    folder_id = '1iBpYTBLHSymzGRkoDPH1I1naL1HTpr2R'
    last_update = dt.strptime('2023-01-01', '%Y-%m-%d')
    files = get_new_files(svc, folder_id, last_update)

    df_concat = pd.DataFrame()
    for file_id in files:
        f = get_file(svc, file_id).decode('utf-8-sig')
        df_raw = pd.DataFrame(StringIO(f))
        df_concat = pd.concat([df_concat, df_raw]).reset_index(drop=True)

    print(df_concat)

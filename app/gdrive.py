# data connection에 last updated 조회하고
# last modified 체크해서, modified > updated인 파일들을 concat -> upsert하기
# 하나의 모듈에 gdrive method 정의하고 나서


from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload
from io import FileIO
import time
import os


def get_gdrive_service():
    docs_path = os.getenv('DOCS_PATH')
    obj = lambda: None
    lmao = {"auth_host_name": 'localhost', 'noauth_local_webserver': 'store_true', 'auth_host_port': [8080, 8090],
            'logging_level': 'ERROR'}
    for k, v in lmao.items():
        setattr(obj, k, v)

    scopes = ['https://www.googleapis.com/auth/drive']
    store = file.Storage(f'{docs_path}/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(f'{docs_path}/client_secret.json', scopes)
        creds = tools.run_flow(flow, store, obj)
    service = build('drive', 'v3', http=creds.authorize(Http()))
    return service


def get_childs(service, folder_id):
    page_token = None
    file_dict = {}
    while True:
        response = service.files().list(q=f"'{folder_id}' in parents",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute()
        for file in response.get('files', []):
            file_dict[file.get('name')] = file.get('id')
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return file_dict


def download_from_gdrive(service, file_id):
    metadata = service.files().get(fileId=file_id).execute()
    file_name = metadata['name']

    # print(metadata['mimeType']) # 파일 형식 체크

    request = service.files().get_media(fileId=file_id)
    fh = FileIO(file_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    time.sleep(0.5)

    return file_path


    # File IO로 다운로드 후 바로 read csv 시도(로컬에 저장 X)

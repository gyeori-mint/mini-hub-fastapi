from app.google_workspace import GoogleDriveApi


if __name__ == '__main__':
    project_id = 'project_bat'
    credential_id = 'google_drive_credential'
    file_id = '1aA4JPW4H6gzsLfb_9XWJnzmakqLYstDh'

    gdrive = GoogleDriveApi(project_id, credential_id)
    file = gdrive.get_file(file_id).decode('utf-8-sig')
    print(file)


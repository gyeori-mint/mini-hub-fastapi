from app.db.models import *


def read_credentials(session, connection_id):
    return [dict(id='meta_credential',
                 connection_id='connection_1')]


def read_datasources(session, credential_id):
    return [dict(id='datasource_1',
                 credential_id='meta_credential',
                 root_key='513038489411939')]


def upsert_data(session, data, service):
    print(data)
    print(service)
    pass

from fastapi import FastAPI
from mangum import Mangum
from connection import meta
from db import crud
from datetime import date
from aws import get_secret

app = FastAPI()

session = ''


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.put("/service/meta")
async def meta_upsert(connection_id: str,
                      start_date: date,
                      end_date: date):
    api = meta.MetaAPI()

    credentials = crud.read_credentials(session, connection_id)

    for cred in credentials:
        secret = get_secret(cred['project_id'], cred['id'])
        api.set_secret(secret)
        datasources = crud.read_datasources(session, cred['id'])

        for ds in datasources:
            rk = ds['root_key']
            data = api.report(rk, start_date, end_date)
            if data:
                crud.upsert_data(session, data, api.service_name)  # csv/json/df 중 output을 어떻게 할지?

    # To-do : credential / datasource의 Success(Timestamp) and Fail 기록

    result = ''
    return result


handler = Mangum(app)

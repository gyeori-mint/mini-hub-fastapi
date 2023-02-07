import boto3
from botocore.exceptions import ClientError
import json

APP_NAME = 'mini-hub'

def get_secret(secret_name, secret_key):
    region_name = "ap-northeast-2"
    secret_id = f'{APP_NAME}/{secret_name}'

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        res = client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = res["SecretString"]

    return json.loads(secret)[secret_key]


def set_secret(secret_name, secret_key, secret_val):
    region_name = "ap-northeast-2"
    secret_id = f'{APP_NAME}/{secret_name}'

    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
    )

    try:
        org_val = json.loads(client.get_secret_value(SecretId=secret_id)['SecretString'])

    except client.exceptions.ResourceNotFoundException:
        org_val = {}
    except:
        raise
    new_secret_val = json.dumps({**org_val, secret_key: secret_val}, default=str)
    try:
        if len(org_val) != 0:
            res = client.put_secret_value(
                SecretId=secret_name,
                SecretString=new_secret_val,
            )
        else:
            res = client.create_secret(
                Name=secret_name,
                SecretString=new_secret_val,
            )
    except ClientError as e:
        raise e

    return res
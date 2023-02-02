import json
import boto3
from botocore.exceptions import ClientError

SECRET = None


def get_secret():
    global SECRET
    if SECRET is None:
        secret_name = "hub-api"
        region_name = "ap-northeast-2"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)

        try:
            res = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        # Decrypts secret using the associated KMS key.
        secret = res["SecretString"]
        SECRET = json.loads(secret)

    return SECRET
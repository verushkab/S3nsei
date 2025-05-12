import os
import boto3
import json


def load_secrets(secret_name, region_name="us-west-2"):
    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)
    secrets = json.loads(response["SecretString"])
    os.environ.update(secrets)  
    return secrets
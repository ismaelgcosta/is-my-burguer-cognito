import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import base64
import urllib.request
import urllib
import json
import os
import re
from urllib.parse import urlencode

USER_POOL_ID = os.environ['USER_POOL_ID']

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    # tratamento para testar via console aws e também rest-api
    if isinstance(event.get('body', event), str) :
        body = json.loads(event.get('body', None))
    else :
        body = event.get('body', event)
        
    try:
        resp = client.admin_disable_user(UserPoolId=USER_POOL_ID, Username=body["username"])
        resp = client.admin_delete_user(UserPoolId=USER_POOL_ID, Username=body["username"])
    except client.exceptions.UserNotFoundException:
        return None, "O usuário não foi encontrado"
    except Exception as e:
        return None, e.__str__()
    return resp, None
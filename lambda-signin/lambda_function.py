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
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

def get_secret_hash(username):
  msg = username + CLIENT_ID 
  dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'),
  msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
  d2 = base64.b64encode(dig).decode()
  return d2
  
def initiate_auth(client, username, password):
    secret_hash = get_secret_hash(username)
    try:
      resp = client.admin_initiate_auth(
                 UserPoolId=USER_POOL_ID,
                 ClientId=CLIENT_ID,
                 AuthFlow='ADMIN_NO_SRP_AUTH',
                 AuthParameters={
                     'USERNAME': username,
                     'SECRET_HASH': secret_hash,
                     'PASSWORD': password,
                  },
                ClientMetadata={
                  'username': username,
                  'password': password,
              })
    except client.exceptions.NotAuthorizedException:
        return None, "O usuário ou senha estão inválidos"
    except client.exceptions.UserNotConfirmedException:
        return None, "O usuário ainda não foi confirmado, verifique seu e-mail"
    except Exception as e:
        return None, e.__str__()
    return resp, None

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    # tratamento para testar via console aws e também rest-api
    if isinstance(event.get('body', event), str) :
        body = json.loads(event.get('body', None))
    else :
        body = event.get('body', event)
    
    for field in ["username", "password"]:
        if not body.get(field, None):
            return {"error": True, "success": False,  'message': f"{field} é obrigatório"}
    username = body['username']
    password = body['password']
                
    resp, msg = initiate_auth(client, username, password)
    
    #return {"error": True, "success": False,  'message': f"{resp} é obrigatório"}
    
    if msg != None:
        return {'message': msg, "error": True, "success": False}
    if resp.get("AuthenticationResult"):
        
        userDetail = client.get_user(AccessToken=resp["AuthenticationResult"]["AccessToken"])
        
        keys = [d['Name'] for d in userDetail["UserAttributes"]]
        values = [d['Value'] for d in userDetail["UserAttributes"]]
        
        for idx, field in enumerate(keys):
            if field == "custom:CPF":
                cpf = values[idx]
            if field == "email":
                email = values[idx]
        
        #print([d['Name'] for d in userDetail["UserAttributes"]])
        print(map(lambda d: d['Name'], userDetail["UserAttributes"]))
        
        return {
                   "statusCode": 200, 
                   "body": json.dumps({
                    "id_token": resp["AuthenticationResult"]["IdToken"],
                    "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                    "access_token": resp["AuthenticationResult"]["AccessToken"],
                    "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                    "token_type": resp["AuthenticationResult"]["TokenType"],
                    "user_detail": {
                        "cpf": cpf,
                        "email": email
                    }
                    }), 
                    "headers": {
                        "content-type": "application/json"
                    }
            }
    else: #this code block is relevant only when MFA is enabled
        return {'body': json.dumps({ "title" : "Request Error", "detail" : "Request Error", "status": 400 }), "statusCode": 400, 
            "headers": {
                "content-type": "application/json"
            }
        }
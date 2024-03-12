import json
import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import uuid
import os

USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode('utf-8'), 
        msg = str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    # tratamento para testar via console aws e também rest-api
    if isinstance(event.get('body', event), str) :
        body = json.loads(event.get('body', None))
    else :
        body = event.get('body', event)
    
    for field in ["username", "password", "code"]:
        if not body.get(field, None):
            return {'body': json.dumps({ "title" : f"{field} é obrigatório", 
                                        "detail" : f"{field} é obrigatório", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }
    username = body['username']
    password = body['password']
    code = body['code']

    try:
        response = client.confirm_sign_up(
        ClientId=CLIENT_ID,
        SecretHash=get_secret_hash(username),
        Username=username,
        ConfirmationCode=code,
        ForceAliasCreation=False,
       )
    except client.exceptions.UserNotFoundException:
        return {'body': json.dumps({ "title" : "O username informado não existe", 
                                        "detail" : "O username informado não existe", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }
    except client.exceptions.CodeMismatchException:
        return {'body': json.dumps({ "title" : "Código de verificação inválido", 
                                        "detail" : "Código de verificação inválido", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }
    except client.exceptions.NotAuthorizedException:
        return {'body': json.dumps({ "title" : "Usuário já confirmado", 
                                        "detail" : "Usuário já confirmado", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }
    except Exception as e:
        return {'body': json.dumps({ "title" : "Erro desconhecido", 
                                        "detail" : f"Erro desconhecido {e.__str__()}", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }
    return {"statusCode": 200, 
                "headers": {
                    "content-type": "application/json"
                }
            }
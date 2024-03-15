import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
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
    
    # tratamento para testar via console aws e também rest-api
    if isinstance(event.get('body', event), str) :
        body = json.loads(event.get('body', None))
    else :
        body = event.get('body', event)
    
    for field in ["username", "email", "password", "name", "cpf"]:
        if not body.get(field, None):
            return {"error": True, "success": False,  'message': f"{field} é obrigatório"}
    
    for field in ["username", "email", "password", "name", "cpf"]:
        if not body.get(field, None):
            return {"error": False, "success": True,  'message': f"{field} é obrigatório", "data": None}
    username = body['username']
    email = body["email"]
    password = body['password']
    name = body["name"]
    cpf = body["cpf"]
    client = boto3.client('cognito-idp')
<<<<<<< Updated upstream
=======
    
    users = getAttributes(get_all_users())
    
    for field in ["username", "email", "password", "name", "cpf"]:
        for idx, user in enumerate(users):
            if body.get(field, None) == user.get(field, None):
                val = body.get(field, None)
                return {'body': json.dumps({ "title" : f"O {field} informado já existe", 
                                        "detail" : f"O {field} informado \"{val}\" já existe", 
                                        "status": 400 }), "statusCode": 400, 
                    "headers": {
                        "content-type": "application/json"
                    }
                }
>>>>>>> Stashed changes

    try:
        response = client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password, 
            UserAttributes=[
            {
                'Name': "name",
                'Value': name
            },
            {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "custom:CPF",
                'Value': cpf
            }
            ],
            ValidationData=[
                {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "custom:username",
                'Value': username
            },
            {
                'Name': "custom:CPF",
                'Value': cpf
            }
])
    
    
    except client.exceptions.UsernameExistsException as e:
        return {"error": False, 
               "success": True, 
               "message": "O username informado já existe", 
               "data": None}
    except client.exceptions.InvalidPasswordException as e:
        
        return {"error": False, 
               "success": True, 
               "message": "Password should have Caps,\
                          Special chars, Numbers", 
               "data": None}
    except client.exceptions.UserLambdaValidationException as e:
        return {"error": False, 
               "success": True, 
               "message": "O E-mail informado já existe", 
               "data": None}
               
    except client.exceptions.InvalidParameterException as e:
        return {"error": False, 
               "success": True, 
               "message": "O CPF informado está em um formato ou tamanho inválido", 
               "data": None}
    
    
    except Exception as e:
        return {"error": False, 
                "success": True, 
                "message": str(e), 
               "data": None}
    
    return {"error": False, 
            "success": True, 
            "message": "Por favor, confirme seu cadastro, verifique o código de autenticação na sua caixa de E-mail", 
            "data": None}
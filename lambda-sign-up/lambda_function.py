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
    
def get_all_users():
    cognito = boto3.client('cognito-idp')
    
    users = []
    next_page = None
    kwargs = {
        'UserPoolId': USER_POOL_ID
    }

    users_remain = True
    while users_remain:
        if next_page:
            kwargs['PaginationToken'] = next_page
        response = cognito.list_users(**kwargs)
        users.extend(response['Users'])
        next_page = response.get('PaginationToken', None)
        users_remain = next_page is not None

    return users
    
def getAttributes(usersDetails):
    users = []

    if usersDetails <> None:
        for idx, user in enumerate(usersDetails):
            keys = [d['Name'] for d in user["Attributes"]]
            values = [d['Value'] for d in user["Attributes"]]
                
            for idx, field in enumerate(keys):
                if field == "custom:CPF":
                    cpf = values[idx]
                if field == "email":
                    email = values[idx]
            users.append({
                "cpf" : cpf,
                "email" : email
            })

    return users
    
def lambda_handler(event, context):
    
    # tratamento para testar via console aws e também rest-api
    if isinstance(event.get('body', event), str) :
        body = json.loads(event.get('body', None))
    else :
        body = event.get('body', event)
    
    for field in ["username", "email", "password", "name", "cpf"]:
        if not body.get(field, None):
            return {'body': json.dumps({ "title" : f"{field} é obrigatório", 
                                        "detail" : f"{field} é obrigatório", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }

    username = body['username']
    email = body["email"]
    password = body['password']
    name = body["name"]
    cpf = body["cpf"]
    client = boto3.client('cognito-idp')
    
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
    
    return f"{users}"

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
                'Name': "username",
                'Value': username
            },
            {
                'Name': "custom:CPF",
                'Value': cpf
            }
])
    
    
    except client.exceptions.UsernameExistsException as e:
        return {'body': json.dumps({ "title" : "O username informado já existe", 
                                        "detail" : "O username informado já existe", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }    
    except client.exceptions.InvalidPasswordException as e:
        return {'body': json.dumps({ "title" : "A senha deve ter letras maiúsculas, símbolos e números", 
                                        "detail" : "O username informado já existe", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }
    except client.exceptions.UserLambdaValidationException as e:
        return {'body': json.dumps({ "title" : "O E-mail informado já existe", 
                                        "detail" : "O E-mail informado já existe", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }
               
    except client.exceptions.InvalidParameterException as e:
        return {'body': json.dumps({ "title" : "O CPF informado está em um formato ou tamanho inválido", 
                                        "detail" : "O CPF informado está em um formato ou tamanho inválido", 
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
    return {'body': json.dumps({
                    "message": "Por favor, confirme seu cadastro, verifique o código de autenticação na sua caixa de E-mail"
            }), "statusCode": 200,
            "headers": {
                "content-type": "application/json"
            }
        }
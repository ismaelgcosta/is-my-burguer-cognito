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

def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    
    if (not event.get("headers", None)) or (not event.get("headers", None).get("authorization", None)):
        return {'body': json.dumps({ "title" : "Request Error", "detail" : "Token not found", "status": 400 }), "statusCode": 400, 
            "headers": {
                "content-type": "application/json"
            }
        }
        
    token = event.get("headers", None).get("authorization", None).replace("Bearer", "" ).replace(" ", "" )
    try:
        resp = client.get_user(AccessToken=token)
                
        val = {'body': json.dumps(resp), "statusCode": 200, 
            "headers": {
                "content-type": "application/json"
            }
        }            
        
        keys = [d['Name'] for d in resp["UserAttributes"]]
        values = [d['Value'] for d in resp["UserAttributes"]]
        
        for idx, field in enumerate(keys):
            if field == "custom:CPF":
                cpf = values[idx]
            if field == "preferred_username":
                preferred_username = values[idx]
            if field == "email":
                email = values[idx]
            if field == "name":
                name = values[idx]
                
        return {'body': json.dumps({
                            "username": resp["Username"],
                            "cpf": cpf,
                            "preferredUsername": preferred_username,
                            "name": name,
                            "email": email
                        }), "statusCode": 200, 
            "headers": {
                "content-type": "application/json"
            }
        }
    except Exception as e:
        return {'body': json.dumps({ "title" : "Request Error", "detail" : f"{e.reason}", "status": 400 }), "statusCode": 400, 
            "headers": {
                "content-type": "application/json"
            }
        }
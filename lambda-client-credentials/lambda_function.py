import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import base64
import urllib.request
import json
import os
from urllib.parse import urlencode


CLIENT_DOMAIN = os.environ['CLIENT_DOMAIN']
CLIENT_RESOURCE_SERVER = os.environ['CLIENT_RESOURCE_SERVER']

def lambda_handler(event, context):
    
    # tratamento para testar via console aws e também rest-api
    if isinstance(event.get('body', event), str) :
        body = json.loads(event.get('body', None))
    else :
        body = event.get('body', event)
        
    for field in ["client_id", "client_secret"]:
        if not body.get(field, None):
            return {'body': json.dumps({ "title" : f"{field} é obrigatório", 
                                        "detail" : f"{field} é obrigatório", 
                                        "status": 400 }), "statusCode": 400, 
                "headers": {
                    "content-type": "application/json"
                }
            }

    client_id = body['client_id']
    client_secret = body['client_secret']
        
    oauth_base_url = f"https://{CLIENT_DOMAIN}.auth.us-east-1.amazoncognito.com/oauth2/token"
    grant_type = "client_credentials"
    scope = f"{CLIENT_RESOURCE_SERVER}/write"  # defined in Cognito
    
    # Base64 encode auth info and add to headers
    auth_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode())
    oauth_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_b64.decode('utf-8')}",
    }

    # Post returns JSON with "access_token" as the Bearer token.
    oauth_payload = { 'grant_type': grant_type,
                      'client_id': client_id,
                      'scope': scope
    }
    
    req = urllib.request.Request(oauth_base_url)
    req.add_header( "Content-Type", "application/x-www-form-urlencoded")
    req.add_header( "Authorization", f"Basic {auth_b64.decode('utf-8')}")
    try:
        resp = urllib.request.urlopen(req, urlencode(oauth_payload).encode()).read().decode('utf-8')
        return {'body': resp, "statusCode": 200, 
        "headers": {
            "content-type": "application/json"
        }}
    except urllib.error.HTTPError as e:
        return {'body': json.dumps({ "title" : e.reason, "detail" : e.reason, "status": e.code }), "statusCode": e.code, 
        "headers": {
            "content-type": "application/json"
        } 
    }
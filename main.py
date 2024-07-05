
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import requests
import os
from token_validation import validate_okta_jwt

app = FastAPI()

# Okta configuration
"""
OKTA_DOMAIN = "https://dev-21414807.okta.com"
INTROSPECT_URL = f"{OKTA_DOMAIN}/oauth2/default/v1/introspect"
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
AUDIENCE='api://default'
"""

OKTA_DOMAIN = "https://dev-21414807.okta.com"
CLIENT_ID = '0oahu6yj0ySOUH1JN5d7'
CLIENT_SECRET = 'dNRmSZJcitlpUmHCQ9ZSAkmjRvE3dlzqEGE0LVvqX4dMdklTevxVkDrUOyFBTKgb'
# TOKEN_URL = f"{OKTA_DOMAIN}/oauth2/test/v1/token"
AUDIENCE='api://test'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Introspect token
def introspect_token(token: str):
    response = requests.post(INTROSPECT_URL, data={
        'token': token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    response.raise_for_status()
    return response.json()

# Token validation dependency
# def validate_token(token: str = Depends(oauth2_scheme)):
#     token_info = introspect_token(token)
#     if not token_info['active']:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return token_info

def validate_token(token: str = Depends(oauth2_scheme)):
    validated_token = validate_okta_jwt(token=token, okta_domain=OKTA_DOMAIN, audience=AUDIENCE)
    if not validated_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return validated_token

# Secure endpoint
@app.get("/data")
def get_data(token_info: dict = Depends(validate_token)):
    return {"message": "Data from Backend 2"}

# To run this backend:
# uvicorn backend2:app --reload --port 8001


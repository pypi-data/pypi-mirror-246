import os
import requests
import base64
import logging
import keyring

from axya_whisper.constants import GENIUS_API_COMPANY_CODE, GENIUS_API_PASSWORD, GENIUS_API_LOGIN, GENIUS_API_URL, SERVICE_CACHE_KEY


# Get the token
token = keyring.get_password('my_service', 'token')
logger = logging.getLogger("app.geniuserp")
logger.setLevel(logging.DEBUG)



def request_access_token(token_endpoint, payload):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer",
    }
    return requests.post(token_endpoint, headers=headers, json=payload)


def decode_base64(base64_string):
    decoded_bytes = base64.b64decode(base64_string)
    return decoded_bytes.decode("utf-8")


def generate_payload():
    return {"CompanyCode": GENIUS_API_COMPANY_CODE, "Password": GENIUS_API_PASSWORD, "Username": GENIUS_API_LOGIN}


def validate_access_token(access_token, token_endpoint):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(token_endpoint, headers=headers)
    return response.status_code == 200


def get_access_token():
    access_token = keyring.get_password(SERVICE_CACHE_KEY, 'token')

    token_endpoint = f"{GENIUS_API_URL}/auth?license=WebServices"

    if access_token and validate_access_token(access_token, token_endpoint):
        logger.info("Getting cached token...")
        return access_token

    logger.info(f"Acquiring new token {token_endpoint}")
    # If the access token is not present or invalid, generate a new one
    payload = generate_payload()
    response = request_access_token(token_endpoint, payload)

    if response.status_code == 200:
        bearer_token = response.json().get("Result")
        keyring.set_password(SERVICE_CACHE_KEY, 'token', bearer_token)
        return bearer_token
    else:
        return None

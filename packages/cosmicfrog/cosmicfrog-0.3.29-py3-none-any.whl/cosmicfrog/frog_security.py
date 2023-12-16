import os
import requests
from typing import Dict
from fastapi import Request, HTTPException
import traceback

# Functions to facilitate API security with Optilogic platform - Use 'optilogic' library

# TODO: move to cosmicfrog
# TODO: Convert all to async with httpx
# TODO: Convert print to logging

def __make_header__(app_key: str, api_key: str, bearer_token: str) -> Dict[str, str]:
    
    if not(app_key or api_key or bearer_token):
        print("Warning: No authorization was provided")
        return False

    base_url = os.getenv("ATLAS_API_BASE_URL")

    if not base_url:
        print("ATLAS_API_BASE_URL is not configured")
        return None

    # set up header with app key or api key depending on value set
    if app_key:
        header_key = "X-APP-KEY"
    else:
        header_key = 'X-API-KEY'

    return {header_key : app_key or api_key or bearer_token.replace("Bearer ","")}


def __get_account__(app_key: str, api_key: str, bearer_token: str):

    try:
        base_url = os.getenv("ATLAS_API_BASE_URL")

        if not base_url:
            print("Error: ATLAS_API_BASE_URL is not defined")
            return False

        new_headers = __make_header__(app_key, api_key, bearer_token)

        if not new_headers:
            print("Error: Unable to create authentication header")
            return False
    
        url = f'{base_url.strip("/")}/account'
        response = requests.request('GET', url, headers = new_headers)

        response.raise_for_status()

        return response.json()
    
    except:
        return None
    


def __authenticate__(app_key: str, api_key: str, bearer_token: str):

    try:
        account = __get_account__(app_key, api_key, bearer_token)

        assert account

        return True

    except:
        traceback.print_exc()
        return False


def __get_app_key__(app_key: str, api_key: str, bearer_token: str):

    # Note: Don't rely on this for security since it can just return the app key it was given
    # For endpoint security use an _authenticate_ method
    if app_key:
        return app_key

    try:
        token_url = os.getenv("FROG_TOKEN_URL")
        
        if not token_url:
            print("FROG_TOKEN_URL is not configured")
            return None

        headers = __make_header__(None, api_key, bearer_token)

        if bearer_token:
            headers = {
                "authorization": bearer_token
            }

        print(f"Calling token service with headers = {headers}")

        response = requests.request('GET', token_url, headers = headers)

        response.raise_for_status()

        appkey = response.json()['appKey']

        return appkey

    except Exception as e:
        print(f"exception getting token {e}")
        return None


# The following are for back compat, they call functions above, but assume you have a request header

# mixed case on purpose. flask supports this for getting keys
# since we are relying on this make it break pretty quick if
# something changes
 
def __check_key__(headers):

    app_key = headers.get("X-App-KEY", None)
    api_key = headers.get("X-Api-KEY", None)
    bearer_token = headers.get("Authorization", None)

    return __authenticate__(app_key, api_key, bearer_token)

def GetUserAccount(headers):

    app_key = headers.get("X-App-KEY", None)
    api_key = headers.get("X-Api-KEY", None)
    bearer_token = headers.get("Authorization", None)

    return __get_account__(app_key, api_key, bearer_token)

def GetUserToken(headers):

    app_key = headers.get("X-App-KEY", None)
    api_key = headers.get("X-API-KEY", None)
    bearer_token = headers.get("Authorization", None)

    return __get_app_key__(app_key, api_key, bearer_token)


# Used for fast api endpoints
def is_secured(request: Request):
    if not __check_key__(request.headers):
        raise HTTPException(status_code=401, detail="Not authorized")
    return True

# Used for socket.io
def socket_secured(app_key: str, api_key: str, bearer_token: str):
    if not __authenticate__(app_key, api_key, bearer_token):
        raise HTTPException(status_code=401, detail="Not authorized")
    return True
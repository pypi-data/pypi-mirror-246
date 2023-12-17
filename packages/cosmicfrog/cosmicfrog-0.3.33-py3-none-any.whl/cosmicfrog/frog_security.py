"""
    Functions for service authentication
"""
from typing import Dict
import os
import traceback
from fastapi import Request, HTTPException
import httpx
import jwt
from .sync_wrapper import sync_wrapper

# Environment
SECURITY_TIMEOUT = os.getenv("SECURITY_TIMEOUT") or 10.0
ADMIN_APP_KEY = os.getenv("ADMIN_APP_KEY")  # Note: Deliberate, no defaults for urls
ATLAS_SERVICE_URL = os.getenv("ATLAS_SERVICE_URL")
ATLAS_API_BASE_URL = os.getenv("ATLAS_API_BASE_URL")


def validate_jwt(jwt_token):
    """
    Offline validation for api token
    This will throw DecodeError if token cannot be decoded
    """
    jwt.decode(jwt_token, options={"verify_signature": False})


def validate_bearer_token(bearer_token):
    """
    Fast offline validation of bearer token
    Will throw if invalid, else can be checked online
    """
    assert bearer_token is not None, "Bearer token is missing"
    assert bearer_token.startswith("Bearer "), "Bearer token is missing prefix"
    jwt_token = bearer_token[7:]
    validate_jwt(jwt_token)


def extract_credentials(*args):
    """
    Utility to support calling security related functions with a header or individual keys
    """
    if len(args) == 1 and hasattr(args[0], 'get'):
        headers = args[0]
        app_key = headers.get("X-App-KEY", None)
        api_key = headers.get("X-API-KEY", None)
        bearer_token = headers.get("Authorization", None)
    else:
        app_key, api_key, bearer_token = args

    return app_key, api_key, bearer_token


def __make_header__(app_key: str, api_key: str, bearer_token: str) -> Dict[str, str]:
    """
    Create header for platform api calls
    """

    if not (app_key or api_key or bearer_token):
        assert False, "No authentication was provided (all keys empty)"

    # Basic bearer key validation
    if not (app_key or api_key):
        assert bearer_token.startswith(
            "Bearer "
        ), "Malformed bearer token, missing Bearer prefix"
        jwt_token = bearer_token[7:]
        jwt.decode(jwt_token, options={"verify_signature": False})

    base_url = os.getenv("ATLAS_API_BASE_URL")

    assert base_url

    # set up header with app key or api key depending on value set
    if app_key:
        header_key = "X-APP-KEY"
    else:
        header_key = "X-API-KEY"

    return {header_key: app_key or api_key or bearer_token.replace("Bearer ", "")}


async def __get_app_key_async__(*args):
    """
    Given an api key or bearer token, fetch an app key
    """

    assert ADMIN_APP_KEY, "ADMIN_APP_KEY is not configured"
    assert ATLAS_SERVICE_URL, "ATLAS_SERVICE_URL is not configured"

    app_key, api_key, bearer_token = extract_credentials(*args)

    if app_key:
        return app_key

    if not api_key:
        validate_bearer_token(bearer_token)
        api_key = bearer_token.replace("Bearer ", "")
    else:
        validate_jwt(api_key)

    # Ensure valid before using contents of token
    if await __authenticate__async(*args) is False:
        raise ValueError("Cannot get app key, invalid authentication key")

    # Get client ID from the token
    decoded_data = jwt.decode(api_key, options={"verify_signature": False})

    data = {"userId": decoded_data["sub"], "name": "Issuing Cosmic Frog key"}

    headers = {"x-app-key": ADMIN_APP_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ATLAS_SERVICE_URL}", headers=headers, json=data, timeout=SECURITY_TIMEOUT
        )

        if response.status_code != 200:
            raise ValueError(f"Failed to get a token: {response.content}")

        return response.json().get("appkey")


__get_app_key__ = sync_wrapper(__get_app_key_async__)


async def __get_account_async__(*args):
    """
    Fetch account details from platform
    """

    assert ATLAS_API_BASE_URL, "ATLAS_API_BASE_URL is not configured"

    app_key, api_key, bearer_token = extract_credentials(*args)

    new_headers = __make_header__(app_key, api_key, bearer_token)

    url = f'{ATLAS_API_BASE_URL.strip("/")}/account'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=new_headers)

        if response.status_code != 200:
            raise ValueError(f"Failed to get account detail: {response.content}")

        return response.json()


__get_account__ = sync_wrapper(__get_account_async__)


async def __authenticate__async(app_key: str, api_key: str, bearer_token: str):
    try:
        account = await __get_account_async__(app_key, api_key, bearer_token)

        assert account

        return True

    # TODO: Likely ok to not catch here, verify in services before removing
    except:
        traceback.print_exc()
        return False


__authenticate__ = sync_wrapper(__authenticate__async)

# The following are for back compat, they call functions above, but assume you have a request header

# mixed case on purpose. flask supports this for getting keys
# since we are relying on this make it break pretty quick if
# something changes


# Following are now all redundant and deprecated in favour of direct calls to above
# TODO: Remove these from clients and remove from here


async def __check_key__async(headers):
    app_key = headers.get("X-App-KEY", None)
    api_key = headers.get("X-Api-KEY", None)
    bearer_token = headers.get("Authorization", None)

    return await __authenticate__async(app_key, api_key, bearer_token)


__check_key__ = sync_wrapper(__check_key__async)


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


async def is_secured_async(request: Request):
    """
    Used for fast api endpoints
    """
    if not await __check_key__async(request.headers):
        raise HTTPException(status_code=401, detail="Not authorized")
    return True


is_secured = sync_wrapper(is_secured_async)


async def socket_secured_async(app_key: str, api_key: str, bearer_token: str):
    """
    Used for socket.io
    """
    if not await __authenticate__async(app_key, api_key, bearer_token):
        raise HTTPException(status_code=401, detail="Not authorized")
    return True


socket_secured = sync_wrapper(socket_secured_async)

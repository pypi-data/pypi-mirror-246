"""
    Wrap platform calls related to model database
"""
import os
import httpx

ATLAS_API_BASE_URL = os.getenv("ATLAS_API_BASE_URL")


async def query_storage(app_key: str, storage_name: str):
    assert ATLAS_API_BASE_URL

    url = ATLAS_API_BASE_URL + f"/storage/{storage_name}/connection-string"

    async with httpx.AsyncClient() as client:
        # Call the API to check the status of the job
        headers = {"X-App-KEY": app_key}
        return await client.get(url, headers=headers)


async def get_db_id(app_key: str, storage_name: str):
    result = await query_storage(app_key, storage_name)

    if result.status_code != 200:
        return None

    return result.json()["raw"]["dbname"]

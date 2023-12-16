import os
import httpx

def get_platform_base_url():

    base_url = os.getenv("ATLAS_API_BASE_URL")

    if not base_url:
        raise EnvironmentError("Environment variable 'ATLAS_API_BASE_URL' is not set.")
 
    base_url = base_url.strip()
    base_url = base_url.strip("/")

    if not base_url:
        raise EnvironmentError("Environment variable 'ATLAS_API_BASE_URL' was empty.") 
    
    return base_url.strip()

async def query_storage(app_key: str, storage_name: str):

    base_url = get_platform_base_url()

    url = base_url + f'/storage/{storage_name}/connection-string'

    async with httpx.AsyncClient() as client:
        # Call the API to check the status of the job
        headers = {'X-App-KEY': app_key}
        return await client.get(url, headers=headers)

async def get_db_id(app_key: str, storage_name: str):

    result = await query_storage(app_key, storage_name)

    if result.status_code != 200:
        return None
    
    return result.json()["raw"]["dbname"]
from requests.auth import HTTPBasicAuth
import requests
import os

from aura.config_repository import load_config
from aura.error_handler import NoCredentialsConfigured
from aura.token_repository import check_existing_token, delete_token_file, save_token

DEFAULT_BASE_URL = "https://api-dev.neo4j-dev.io/harsha/v1beta3"
DEFAULT_AUTH_URL = 'https://api-dev.neo4j-dev.io/harsha-oauth/token'

def _get_credentials():
    client_id = os.environ.get("AURA_CLI_CLIENT_ID")
    client_secret = os.environ.get("AURA_CLI_CLIENT_SECRET")
    if not client_id or not client_secret:
        config = load_config()
        
        if config.get("AUTH", None) is None or config["AUTH"].get("ACTIVE", None) is None:
            raise NoCredentialsConfigured("No credentials configured. Either add new credentials or export environment variables.")
        
        active_credentials = config["AUTH"]["ACTIVE"]
        client_id = client_id or config["AUTH"]["CREDENTIALS"][active_credentials]["CLIENT_ID"]
        client_secret = client_secret or config["AUTH"]["CREDENTIALS"][active_credentials]["CLIENT_SECRET"]

    return client_id, client_secret

def _authenticate():
    token = check_existing_token()
    if token:
        return token

    client_id, client_secret = _get_credentials()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials'
    }

    url = os.environ.get("AURA_CLI_AUTH_URL") or DEFAULT_AUTH_URL
    response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    token, expires_in = response.json()["access_token"], response.json()["expires_in"]

    save_token(token, expires_in)

    return token


def _get_headers():
    token = _authenticate()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return headers

def make_api_call(method, path, **kwargs):
    headers = _get_headers()
    base_url = os.environ.get("AURA_CLI_BASE_URL") or DEFAULT_BASE_URL

    response = requests.request(method, base_url+path, headers=headers, **kwargs)
    # If authentication failed, delete the token file to avoid using same token again
    if response.status_code  in [401, 403]:
        delete_token_file()

    response.raise_for_status()

    return response.json()


from requests.auth import HTTPBasicAuth
import requests
import os

from aura.config_repository import load_config

DEFAULT_BASE_URL = "https://api-dev.neo4j-dev.io/harsha/v1beta3"
DEFAULT_AUTH_URL = 'https://api-dev.neo4j-dev.io/harsha-oauth/token'

def _get_credentials():
    client_id = os.environ.get("AURA_CLI_CLIENT_ID")
    client_secret = os.environ.get("AURA_CLI_CLIENT_SECRET")
    if not client_id or not client_secret:
        config = load_config()
        active_credentials = config["AUTH"]["ACTIVE"]
        client_id = client_id or config["AUTH"]["CREDENTIALS"][active_credentials]["CLIENT_ID"]
        client_secret = client_secret or config["AUTH"]["CREDENTIALS"][active_credentials]["CLIENT_SECRET"]

    return client_id, client_secret

def _authenticate():
    # TODO check if valid token exists first
    # If yes use is
    # if not, continue as before and save new token
    # TODO need to check if token belongs to current credentials? Because after switching the token will be invalid
    # Or always try old token first and if not working then get new token

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

    # TODO save new Token

    return token

def _get_headers():
    token = _authenticate()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return headers

# TODO some endpoints like resume and pause dont return data/json ?
def make_api_call(method, path, **kwargs):
    headers = _get_headers()
    base_url = os.environ.get("AURA_CLI_BASE_URL") or DEFAULT_BASE_URL

    response = requests.request(method, base_url+path, headers=headers, **kwargs)
    response.raise_for_status()

    return response.json()
from requests.auth import HTTPBasicAuth
import requests
import os

from aura.config_repository import load_config

DEFAULT_BASE_URL = "https://api-dev.neo4j-dev.io/harsha/v1beta3"
DEFAULT_AUTH_URL = 'https://api-dev.neo4j-dev.io/harsha-oauth/token'

def _get_credentials():
    config = load_config()
    client_id = os.environ.get("AURA_API_CLIENT_ID") or config["AUTH"]["CLIENT_ID"]
    client_secret = os.environ.get("AURA_API_CLIENT_SECRET") or config["AUTH"]["CLIENT_SECRET"]

    return client_id, client_secret

def _authenticate():
    client_id, client_secret = _get_credentials()

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials'
    }

    url = os.environ.get("AURA__API_AUTH_URL") or DEFAULT_AUTH_URL
    response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    return response.json()["access_token"]

def _get_headers():
    token = _authenticate()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return headers

def make_api_call(method, path, **kwargs):
    headers = _get_headers()
    base_url = os.environ.get("AURA_API_BASE_URL") or DEFAULT_BASE_URL

    response = requests.request(method, base_url+path, headers=headers, **kwargs)
    response.raise_for_status()

    return response.json()
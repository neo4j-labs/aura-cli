from requests.auth import HTTPBasicAuth
import requests
import configparser
import os

#BASE_URL = "https://api-bryce3.neo4j-dev.io/v1beta3/"
BASE_URL = "https://api-dev.neo4j-dev.io/harsha/v1beta3"
#AUTH_URL = 'https://api.neo4j.io/aura-oauth/token'
#AUTH_URL = 'https://api-bryce3.neo4j-dev.io/oauth/token'
AUTH_URL = 'https://api-dev.neo4j-dev.io/harsha-oauth/token'

def read_config():
    config = configparser.ConfigParser()
    config_path = os.path.expanduser('~/.aura/config.ini')
    config.read(config_path)
    return config

def write_config(config):
    config_path = os.path.expanduser('~/.aura/config.ini')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def authenticate():
    config = read_config()
    client_id, client_secret = config["AUTH"]["CLIENT_ID"], config["AUTH"]["CLIENT_SECRET"]

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(AUTH_URL, headers=headers, data=data, auth=HTTPBasicAuth(client_id, client_secret))
    return response.json()["access_token"]

def get_headers():
    token = authenticate()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    return headers

def make_api_call(method, path, **kwargs):
    headers=get_headers()
    response = requests.request(method, BASE_URL+path, headers=headers, **kwargs)
    response.raise_for_status()
    return response.json()
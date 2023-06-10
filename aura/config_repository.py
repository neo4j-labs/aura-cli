import json
import os

from aura.token_repository import delete_token_file

AURA_CONFIG_PATH = '~/.aura/config.json'

# TODO add exceptions such as CredentialsNotFound, 
# TODO validate config format on every load

def load_config():
    config_path = os.path.expanduser(AURA_CONFIG_PATH)

    try:
        with open(config_path, 'r') as configfile:
            config = json.load(configfile)
    except FileNotFoundError:
        config = {}
        write_config(config)
    
    return config

def write_config(config):
    config_path = os.path.expanduser(AURA_CONFIG_PATH)
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    with open(config_path, 'w') as configfile:
        json.dump(config, configfile)


def list_credentials():
    config = load_config()
    if config.get("AUTH") and config["AUTH"].get("CREDENTIALS"):
        credentials = config["AUTH"].get("CREDENTIALS")
        return [{"Name": c, "ClientId": credentials[c]["CLIENT_ID"]} for c in credentials.keys()]

    return []


def add_credentials(name, client_id, client_secret):
    config = load_config()
    if not config.get("AUTH"):
        config["AUTH"] = {"CREDENTIALS": {}, "ACTIVE": None}
    
    config["AUTH"]["CREDENTIALS"][name] = {}

    config["AUTH"]["CREDENTIALS"][name]["CLIENT_ID"] = client_id
    config["AUTH"]["CREDENTIALS"][name]["CLIENT_SECRET"] = client_secret
    config["AUTH"]["ACTIVE"] = name
    
    write_config(config)

    # Delete saved auth token if it exists
    delete_token_file()


def current_credentials():
    config = load_config()
    if config.get("AUTH") and config["AUTH"].get("ACTIVE"):
        active = config["AUTH"].get("ACTIVE")
        return active, config["AUTH"]["CREDENTIALS"][active]["CLIENT_ID"]


def delete_credentials(name):
    config = load_config()
    if config.get("AUTH") and config["AUTH"].get("CREDENTIALS") and config["AUTH"]["CREDENTIALS"][name]:
        del config["AUTH"]["CREDENTIALS"][name]
        write_config(config)


def use_credentials(name):
    config = load_config()
    if config.get("AUTH") and config["AUTH"].get("CREDENTIALS") and config["AUTH"]["CREDENTIALS"][name]:
        config["AUTH"]["ACTIVE"] = name
        write_config(config)

        # Delete saved auth token if it exists
        delete_token_file()



"""This module defines methods for making HTTP request to the Aura API"""
import os
import json
import click
from requests.auth import HTTPBasicAuth
import requests

from aura.config_repository import CLIConfig
from aura.version import __version__
from aura.logger import get_logger
from aura.error_handler import NoCredentialsConfigured
from aura.token_repository import (
    check_existing_token,
    delete_token_file,
    save_token,
)


def _get_credentials():
    logger = get_logger()

    client_id = os.environ.get("AURA_CLI_CLIENT_ID")
    client_secret = os.environ.get("AURA_CLI_CLIENT_SECRET")

    if client_id:
        logger.debug("Reading API client id from environment variable AURA_CLI_CLIENT_ID.")
    if client_secret:
        logger.debug("Reading API client secret from environment variable AURA_CLI_CLIENT_SECRET.")

    if not client_id or not client_secret:
        ctx = click.get_current_context()
        config = ctx.obj
        cred_name, current_credentials = config.current_credentials()

        if current_credentials is None:
            raise NoCredentialsConfigured()

        if not client_id:
            logger.debug(f"Reading API client id from configured credentials {cred_name}.")
        if not client_secret:
            logger.debug(f"Reading API client secret from configured credentials {cred_name}.")

        client_id = client_id or current_credentials["CLIENT_ID"]
        client_secret = client_secret or current_credentials["CLIENT_SECRET"]

    if not client_id or not client_secret:
        logger.warning("No API credentials were configured.")
        raise NoCredentialsConfigured()

    return client_id, client_secret


def _authenticate():
    logger = get_logger()
    logger.debug("Checking for existing API token.")

    token = check_existing_token()
    if token:
        logger.debug("API token found. Using existing token for authentication.")
        return token

    client_id, client_secret = _get_credentials()

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": f"AuraCLI/{__version__}",
    }
    data = {"grant_type": "client_credentials"}

    ctx = click.get_current_context()
    config: CLIConfig = ctx.obj
    # Get url by priority: First by env var, then by config setting, then by default url
    url = config.env["auth_url"]

    logger.debug("No token found. Requesting new token from " + url)

    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=data,
        auth=HTTPBasicAuth(client_id, client_secret),
        timeout=10,
    )
    try:
        response.raise_for_status()
    except Exception as e:
        logger.warning("Authentication request was not succesful.")
        raise e

    logger.debug("Authentication request successful. Using new auth token.")

    token, expires_in = (
        response.json()["access_token"],
        response.json()["expires_in"],
    )
    save_token(token, expires_in)

    return token


def get_headers():
    """Returns the HTTP headers used for Aura API requests"""

    token = _authenticate()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "User-Agent": f"AuraCLI/{__version__}",
    }
    return headers


def make_api_call(method: str, path: str, **kwargs):
    """Make a HTTP request to the Aura API"""

    ctx = click.get_current_context()
    config: CLIConfig = ctx.obj
    logger = get_logger()

    headers = get_headers()

    # Get url by priority: First by env var, then by config setting, then by default url
    base_url = config.env["base_url"]
    full_url = base_url + path

    logger.debug(f"Initializing connection to Aura Cloud Platform API endpoint: {base_url}")
    data_string = " with data: " + json.dumps(kwargs["data"]) if "data" in kwargs else ""
    logger.debug(f"Sending {method} request to {full_url}{data_string}")

    response = requests.request(method, full_url, headers=headers, timeout=10, **kwargs)
    # If authentication failed, delete the token file to avoid using same token again
    if response.status_code in [401, 403]:
        logger.warning("API authentication failed.")
        delete_token_file()

    return response

import os
import subprocess
import json

from .helpers import validate_json_output

DEFAULT_BASE_URL = "https://api.neo4j.io/v1"
DEFAULT_AUTH_URL = "https://api.neo4j.io/oauth/token"

CREDENTIALS_NAME = "prod"
CLI_CONFIG_PATH = "~/.aura/config.json"


def run_cli_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command '{' '.join(command)}' failed: {result.stderr}")
    return result.stdout


def run_release_checks():
    # Read environment variables
    client_id = os.environ.get("AURA_CLI_RELEASE_CHECKS_CLIENT_ID")
    if not client_id:
        raise Exception("No Client Id provided.")

    client_secret = os.environ.get("AURA_CLI_RELEASE_CHECKS_CLIENT_SECRET")
    if not client_secret:
        raise Exception("No Client Secret provided.")

    base_url = os.environ.get("AURA_CLI_RELEASE_CHECKS_BASE_URL") or DEFAULT_BASE_URL
    auth_url = os.environ.get("AURA_CLI_RELEASE_CHECKS_CLIENT_ID") or DEFAULT_AUTH_URL

    test_set_credentials_and_urls(client_id, client_secret, base_url, auth_url)

    validate_config_file(client_id, client_secret, base_url, auth_url)

    tenant_id = test_tenants()

    # TODO create DBs and test list
    # TODO DB one: create, rename, pause, resume
    # TODO DB two: create, resize
    # TODO DB DS: create, resize
    # TODO DB 3: create, list snaps, create snap, get snap, restore snap
    # TODO 4: Create 2 DBs and overwrite instance

    # TODO test get by db name and id. Fails when name not found or duplicate.

    # TODO set default tenant and do some checks
    # TODO set default output and do some gets requests

    # TODO delete dbs / cleanup


def test_set_credentials_and_urls(client_id, client_secret, base_url, auth_url):
    output = run_cli_command(
        [
            "aura",
            "credentials",
            "add",
            "--name",
            CREDENTIALS_NAME,
            "--client-id",
            client_id,
            "--client-secret",
            client_secret,
        ]
    )
    assert (
        output
        == f'Credentials "{CREDENTIALS_NAME}" successfully saved. Now using "{CREDENTIALS_NAME}" as'
        " credentials."
    )

    output = run_cli_command(["aura", "config", "set", "base-url", base_url])
    assert output == f'Config option base-url set to "{base_url}"'

    output = run_cli_command(["aura", "credentials", "set", "auth-url", auth_url])
    assert output == f'Config option auth-url set to "{auth_url}"'


# Validate the CLI config file
def validate_config_file(client_id, client_secret, base_url, auth_url):
    path = os.path.expanduser("~/.aura/config.json")
    with open(path, "r", encoding="utf-8") as configfile:
        config = json.load(configfile)
        validate_json_output(config, schema="config-schema.json", is_json=True)

        assert config["AUTH"]["ACTIVE"] == CREDENTIALS_NAME
        assert config["AUTH"]["CREDENTIALS"][CREDENTIALS_NAME]["CLIENT_ID"] == client_id
        assert config["AUTH"]["CREDENTIALS"][CREDENTIALS_NAME]["CLIENT_SECRET"] == client_secret
        assert config["DEFAULTS"]["BASE_URL"] == base_url
        assert config["DEFAULTS"]["AUTH_URL"] == auth_url


# Test tenants commands
def test_tenants():
    output = run_cli_command(["aura", "tenants", "list"])
    tenants = validate_json_output(output, schema="tenants-list-schema.json")
    assert len(tenants) == 1
    tenant_id = tenants[0]["id"]

    output = run_cli_command(["aura", "tenants", "get", "--tenant-id", tenant_id])
    validate_json_output(output, schema="tenants-get-schema.json")

    return tenant_id


if __name__ == "__main__":
    run_release_checks()

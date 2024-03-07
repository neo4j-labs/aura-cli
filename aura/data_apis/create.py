import json
import click
from aura.api_command import api_command
from aura.api_repository import (
    make_api_call,
    make_api_call_and_wait_for_data_api_status,
)
from graphql import GraphQLError
from aura.data_apis.util.type_definitions import read_and_encode_type_definitions

from aura.error_handler import handle_error


# pylint: disable=redefined-builtin
@api_command(name="create", help_text="Create a new instance")
@click.option("--instance-id", help="The instance ID", required=True)
@click.option("--instance-username", help="The instance username", required=True)
@click.password_option("--instance-password")
@click.option("--name", help="The data API name", required=True)
@click.option(
    "--type",
    default="graphql",
    help="The data API type",
    type=click.Choice(["graphql"]),
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait until instance is created",
)
@click.option("--type-definitions", prompt=True)
@click.option("--jwks-url")
def create_data_api(
    instance_id: str,
    instance_username: str,
    instance_password: str,
    name: str,
    type: str,
    wait: bool,
    type_definitions: str,
    jwks_url: str,
):
    """
    Create a new data API with specified options.

    Makes "POST /instances/:instanceId/data-apis" API request.
    """

    path = f"/instances/{instance_id}/data-apis"

    try:
        type_definitions = read_and_encode_type_definitions(type_definitions)
    except GraphQLError as e:
        handle_error(e)

    data = {
        "name": name,
        "type": type,
        "aura_instance": {"username": instance_username, "password": instance_password},
        "data_api": {"graphql": {"type_definitions": type_definitions}},
    }

    if jwks_url is not None:
        data["security"] = {"jwks": {"url": jwks_url}}

    if wait:
        return make_api_call_and_wait_for_data_api_status(
            "POST", path, "ready", data=json.dumps(data)
        )

    return make_api_call("POST", path, data=json.dumps(data))

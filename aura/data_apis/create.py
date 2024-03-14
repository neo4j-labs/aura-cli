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
@api_command(name="create", help_text="Create a new data API for the given instance")
@click.option(
    "--instance-id",
    help="The ID of the instance for which the data API will be created.",
    required=True,
)
@click.option(
    "--instance-username",
    help="The username which the data API will use to connect to the instance.",
    required=True,
)
@click.password_option(
    "--instance-password",
    help="The password which the data API will use to connect to the instance.",
)
@click.option("--name", help="A friendly name to give to the data API", required=True)
@click.option(
    "--type",
    default="graphql",
    help="The type of data API to be created.",
    type=click.Choice(["graphql"]),
)
@click.option(
    "--type-definitions",
    prompt=True,
    help="The type definitions to use if creating a GraphQL data API. This can be either a path to a file containing type definitions, or type definitions directly into the prompt.",
)
@click.option(
    "--jwks-url",
    help="An optional JWKS URL to be used for authorization features of the data API.",
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait until the data API is ready for use?",
)
def create_data_api(
    instance_id: str,
    instance_username: str,
    instance_password: str,
    name: str,
    type: str,
    type_definitions: str,
    jwks_url: str,
    wait: bool,
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

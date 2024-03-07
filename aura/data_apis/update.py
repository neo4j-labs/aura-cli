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
@api_command(name="update", help_text="Update a data API")
@click.option("--instance-id", help="The instance ID", required=True)
@click.option("--data-api-id", help="The data API ID", required=True)
@click.option("--instance-username", help="The instance username")
@click.option("--instance-password")
@click.option("--name", help="The data API name")
@click.option("--type-definitions")
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait until instance is created",
)
def update_data_api(
    instance_id: str,
    data_api_id: str,
    instance_username: str,
    instance_password: str,
    name: str,
    type_definitions: str,
    wait: bool,
):
    """
    Updates a data API with specified options.

    Makes "PATCH /instances/:instanceId/data-apis/:dataApiId" and/or "PATCH /instances/:instanceId/data-apis/:dataApiId/graphql" API request depending on the input.
    """

    data = {}
    aura_instance = {}

    if name:
        data["name"] = name
    if instance_username:
        aura_instance["username"] = instance_username
    if instance_password:
        aura_instance["password"] = instance_password

    if aura_instance:
        data["aura_instance"] = aura_instance

    if data:
        path = f"/instances/{instance_id}/data-apis/{data_api_id}"

        if wait:
            result = make_api_call_and_wait_for_data_api_status(
                "PATCH", path, "ready", data=json.dumps(data)
            )

        result = make_api_call("PATCH", path, data=json.dumps(data))

    if type_definitions:
        try:
            type_definitions = read_and_encode_type_definitions(type_definitions)
        except GraphQLError as e:
            handle_error(e)

        data = {"type_definitions": type_definitions}

        path = f"/instances/{instance_id}/data-apis/{data_api_id}/graphql"

        if wait:
            result = make_api_call_and_wait_for_data_api_status(
                "PATCH", path, "ready", data=json.dumps(data)
            )

        result = make_api_call("PATCH", path, data=json.dumps(data))

    return result

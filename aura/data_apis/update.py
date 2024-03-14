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
@api_command(name="update", help_text="Update a data API for the given instance")
@click.option(
    "--instance-id",
    help="The ID of the instance associated with the data API.",
    required=True,
)
@click.option(
    "--data-api-id", help="The ID of the data API to be updated.", required=True
)
@click.option(
    "--instance-username",
    help="Update the username which the data API will use to connect to the instance.",
)
@click.option(
    "--instance-password",
    help="Update the password which the data API will use to connect to the instance.",
)
@click.option("--name", help="Update the friendly name for the data API.")
@click.option(
    "--type-definitions",
    help="Update the type definitions to use if this is a GraphQL data API. This can be either a path to a file containing type definitions, or type definitions directly into the prompt.",
)
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait until the data API is ready for use?",
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

    result = {}

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
            type_definitions_result = make_api_call_and_wait_for_data_api_status(
                "PATCH", path, "ready", data=json.dumps(data)
            )

        type_definitions_result = make_api_call("PATCH", path, data=json.dumps(data))

        if not result:
            result = type_definitions_result

    return result

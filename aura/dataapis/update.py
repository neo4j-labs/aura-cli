import json
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command(name="update", help_text="Update a data api")
@click.option("--data-api-id", "-did", prompt=True, help="Mandatory. The ID of the data api to modify")
@click.option("--name", "-n", prompt=True, default="", help="The new data connector name")
@click.option("--instance-id", "-id", prompt=True, default="", help="Updated Aura instance ID to use with this data api")
@click.option("--username", "-u", prompt=True, default="", help="Updated Aura instance DB username to use with this data api")
@click.option("--password", "-p", prompt=True, default="", help="Updated Aura instance DB username to use with this data api")


def update_dataapi(data_api_id: str,
                         name: str,
                         instance_id: str,
                         username : str,
                         password : str):
    """
    Update a data connector.

    Only memory and name can be updated.

    Makes "PATCH /data-connectors/:data connector ID" API request.
    """

    data = {}
    if name:
        data["name"] = name

    if instance_id:
        data["aura_instance"]["id"] = instance_id

    if username:
        data["aura_instance"]["username"] = username

    if password:
        data["aura_instance"]["password"] = password

    path = f"/data-connectors/{data_api_id}"


    return make_api_call("PATCH", path, data=json.dumps(data))


@api_command(name="update_td", help_text="Update a GraphQL data api type definitions")
@click.option("--data-api-id", "-did", prompt=True, help="Mandatory. The ID of the GraphQL data api to modify")
@click.option("--type-defs", "-td", prompt=True, help="The GraphQL type definitions to use with the data api")


def update_dataapi_graphql_td(data_api_id: str,
                         type_defs: str):
    """
    Update type defs for a graphql data api.

    Makes "PATCH /data-connectors/:data connector ID/graphql" API request.
    """

    data = {}

    if type_defs:
        data["type_definitions"] = type_defs

        path = f"/data-connectors/{data_api_id}"

        return make_api_call("PATCH", path, data=json.dumps(data))

    else:
        return {f'No type definitions given for GraphQL API with ID: {data_api_id}'}
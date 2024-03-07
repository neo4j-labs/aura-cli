import click
from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command(name="list", help_text="List all data APIs for a given instance")
@click.option(
    "--instance-id", help="The ID of the instance to list data APIs for.", required=True
)
def list_data_apis(instance_id: str):
    """
    List data APIs of an instance.

    Makes "GET /instances/:instanceId/data-apis" API request.
    """

    path = f"/instances/{instance_id}/data-apis"

    return make_api_call("GET", path)

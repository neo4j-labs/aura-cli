import click
from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command(name="get", help_text="Get details for a specific data API")
@click.option("--instance-id", help="The instance ID", required=True)
@click.option("--data-api-id", help="The data API ID", required=True)
def get_data_api(instance_id: str, data_api_id: str):
    """
    Get details of a data API.

    Makes "GET /instances/:instanceId/data-apis/:dataApiId" API request.
    """

    path = f"/instances/{instance_id}/data-apis/{data_api_id}"

    return make_api_call("GET", path)

import click
from aura.api_command import api_command
from aura.api_repository import make_api_call


# pylint: disable=unused-argument
def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@api_command(
    name="delete", help_text="Delete the given data API for the given instance"
)
@click.option(
    "--instance-id",
    help="The ID of the instance associated with the data API.",
    required=True,
)
@click.option(
    "--data-api-id", help="The ID of the data API to be deleted.", required=True
)
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Are you sure you want to delete the data API?",
    help="Confirmation flag",
)
def delete_data_api(instance_id: str, data_api_id: str):
    """
    Delete a data API.

    Makes "DELETE /instances/:instanceId/data-apis/:dataApiId" API request.
    """

    path = f"/instances/{instance_id}/data-apis/{data_api_id}"
    return make_api_call("DELETE", path)

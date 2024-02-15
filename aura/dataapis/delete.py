import click
from aura.api_command import api_command
from aura.api_repository import make_api_call

# pylint: disable=unused-argument
def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@api_command(name="delete", help_text="Delete a data api")
@click.option("--data-api-id", "-did", prompt=True, help="Mandatory. The ID of the data api to delete")
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Are you sure you want to delete the dataconnector?",
    help="Confirmation flag",
)
def delete_dataapi(data_api_id: str):
    """
    Delete a data api
    Makes "DELETE /data-connectors/:dataConnectorID

    """
    path = f"/data-connectors/{data_api_id}"

    print("At make_api_call")
    api_response = make_api_call("DELETE", path)

    print(api_response)

    return api_response


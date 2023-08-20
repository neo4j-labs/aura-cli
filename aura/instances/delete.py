import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id


# pylint: disable=unused-argument
def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@api_command(name="delete", help_text="Delete an instance")
@click.option("--instance-id", "-id", help="The instance ID")
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Are you sure you want to delete the database?",
    help="Confirmation flag",
)
@click.option("--name", "-n", help="The instance name")
def delete_instance(instance_id: str, name: str):
    """
    Delete an instance.

    Makes "DELETE /instances/:instanceId" API request.
    """

    instance_id = get_instance_id(instance_id, name)

    path = f"/instances/{instance_id}"
    return make_api_call("DELETE", path)

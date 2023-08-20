import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id


@api_command(name="list", help_text="List all snapshots for an instance")
@click.option("--instance-id", "-id", help="The instance ID")
@click.option("--instance-name", "-n", help="The instance name")
@click.option("--date", "-d", help="Optional snapshot date")
def list_snapshots(instance_id: str, instance_name: str, date: str):
    """
    List snapshots of an instance.

    An optional date option can be provided in yyyy-mm-dd format to filter snapshots by date.

    Makes "GET /instances/:instanceId/snapshots" API request.
    """

    instance_id = get_instance_id(instance_id, instance_name)

    path = f"/instances/{instance_id}/snapshots"

    if date:
        path += f"?date={date}"

    return make_api_call("GET", path)

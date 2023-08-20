import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id


@api_command(name="get", help_text="Get details for a specific snapshot")
@click.option("--snapshot-id", "-s", prompt=True, help="The snapshot ID")
@click.option("--instance-name", "-n", help="The instance name")
@click.option("--instance-id", "-id", help="The instance ID")
def get_snapshot(instance_id: str, instance_name: str, snapshot_id: str):
    """
    Get details of a snapshot.

    Makes "GET /instances/:instanceId/snapshots/:snapshotId" API request.
    """

    instance_id = get_instance_id(instance_id, instance_name)

    path = f"/instances/{instance_id}/snapshots/{snapshot_id}"

    return make_api_call("GET", path)

import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id


@api_command(name="restore", help_text="Restore an instance from a snapshot")
@click.option("--instance-id", "-id", help="The instance ID")
@click.option("--instance-name", "-n", help="The instance name")
@click.option("--snapshot-id", "-s", prompt=True, help="The snapshot ID which you want to restore")
def restore_snapshot(instance_id: str, instance_name: str, snapshot_id: str):
    """
    Restore a snapshot of an instance.

    Makes "POST /instances/:instanceId/snapshots/:snapshotId/restore" API request.
    """

    instance_id = get_instance_id(instance_id, instance_name)

    path = f"/instances/{instance_id}/snapshots/{snapshot_id}/restore"

    return make_api_call("POST", path)

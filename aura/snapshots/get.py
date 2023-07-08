from datetime import datetime
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id

# GET /instances/:instanceId/snapshots/:snapshotId

@api_command(help="Get details for a specific snapshot")
@click.option('--snapshot-id', '-s', prompt=True, help="The snapshot ID")
@click.option('--instance-name', '-n', help="The instance name")
@click.option('--instance-id', '-id', help="The instance ID")
def get(instance_id, instance_name, snapshot_id):
    instance_id = get_instance_id(instance_id, instance_name)

    path = f"/instances/{instance_id}/snapshots/{snapshot_id}"

    return make_api_call("GET", path)
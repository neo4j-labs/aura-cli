from datetime import datetime
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id

# GET /instances/:instanceId/snapshots

@api_command(help="List all snapshots for an instance")
@click.option('--instance-id', '-id', help="The instance ID")
@click.option('--instance-name', '-n', help="The instance name")
@click.option('--date', '-d', help="Optional snapshot date")
def list(instance_id, instance_name, date):
    instance_id = get_instance_id(instance_id, instance_name)

    path = f"/instances/{instance_id}/snapshots"

    params = {}
    if date:
        params={"date": date}

    return make_api_call("GET", path, params=params)
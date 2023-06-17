import json
import click
from aura.api_command import api_command

from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id

# POST /instances/:instanceId/overwrite

@api_command(help="Overwrite an instance")
@click.option('--instance-id', '-id', help="The instance ID")
@click.option('--source-instance', '-s', prompt=True, help="The source instance ID from which to overwrite the target")
@click.option('--name', '-n', help="The instance name")
def overwrite(instance_id, source_instance, name):
    instance_id = get_instance_id(instance_id, name)

    data = {"source_instance_id": source_instance}
    path = f"/instances/{instance_id}/overwrite"

    return make_api_call("POST", path, data=json.dumps(data))
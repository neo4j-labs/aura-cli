import json
import click
from aura.api_command import api_command

from aura.api_repository import make_api_call

@api_command
@click.option('--instance-id', '-id', prompt=True)
@click.option('--source-instance-id', '-s', prompt=True)
def overwrite(instance_id, source_instance_id):
    data = {"source_instance_id": source_instance_id}
    path = f"/instances/{instance_id}"

    return make_api_call("POST", path, data=json.dumps(data))
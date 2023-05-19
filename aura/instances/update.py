import json
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command
@click.option('--instance-id', '-id')
@click.option('--memory', '-m')
@click.option('--new-name', '-n')
def update(instance_id, memory, new_name):
    data = {}
    if memory:
        data["memory"] = memory
    if new_name:
        data["name"] = new_name
    path = f"/instances/{instance_id}"

    return make_api_call("PATCH", path, data=json.dumps(data))
import json
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id


@api_command(help="Update an instance")
@click.option('--instance-id', '-id', help="The instance ID")
@click.option('--memory', '-m', help="A new instance memory size (for resizing)")
@click.option('--new-name', help="A new instance name (for renaming)")
@click.option('--name', '-n', help="The instance name")
def update(instance_id, memory, new_name, name):
    instance_id = get_instance_id(instance_id, name)
    
    data = {}
    if memory:
        data["memory"] = memory
    if new_name:
        data["name"] = new_name
    path = f"/instances/{instance_id}"

    return make_api_call("PATCH", path, data=json.dumps(data))
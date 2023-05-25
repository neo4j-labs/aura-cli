import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id

@api_command
@click.option('--instance-id', '-id')
@click.option('--name', '-n')
def get(instance_id, name):
    instance_id = get_instance_id(instance_id, name)

    path = f"/instances/{instance_id}"

    return make_api_call("GET", path)
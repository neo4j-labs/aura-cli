import click
from aura.api_command import api_command
from aura.repository import make_api_call

@api_command
@click.option('--instance-id', '-id', prompt=True)
def get(instance_id):
    path = f"/instances/{instance_id}"

    return make_api_call("GET", path)
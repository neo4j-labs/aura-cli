import click
from aura.api_command import api_command
from aura.repository import make_api_call

@api_command
@click.option('--instance_id', '-id', prompt=True)
def create(instance_id):
    path = f"/instances/{instance_id}/snapshots"

    return make_api_call("POST", path)
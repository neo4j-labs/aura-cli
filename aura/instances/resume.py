import click
from aura.api_command import api_command
from aura.api_repository import make_api_call

@api_command
@click.option('--instance-id', '-id')
def resume(instance_id):
    path = f"/instances/{instance_id}/resume"

    return make_api_call("POST", path)
import click
from aura.api_command import api_command

from aura.repository import make_api_call


@api_command
@click.option('--instance_id', '-id', prompt=True)
@click.option('--snapshot_id', '-s', prompt=True)
def restore(instance_id, snapshot_id):
    path = f"/instances/{instance_id}/snapshots/{snapshot_id}/restore"

    return make_api_call("POST", path)
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@api_command
@click.option('--instance-id', '-id', prompt=True)
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to delete the database?')
def delete(instance_id):
    path = f"/instances/{instance_id}"
    return make_api_call("DELETE", path)
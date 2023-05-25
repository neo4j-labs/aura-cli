import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@api_command
@click.option('--instance-id', '-id')
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to delete the database?')
@click.option('--name', '-n')
def delete(instance_id, name):
    instance_id = get_instance_id(instance_id, name)
    
    path = f"/instances/{instance_id}"
    return make_api_call("DELETE", path)
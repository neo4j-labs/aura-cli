import click
from aura.api_command import api_command
from aura.repository import make_api_call


@api_command
@click.option('--tenant_id', '-tid')
def list(tenant_id):
    params=None
    if tenant_id is not None:
        params={"tenant_id": tenant_id}
    path = "/instances"
    
    return make_api_call("GET", path, params=params)
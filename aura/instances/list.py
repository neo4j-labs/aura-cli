import click
from aura.api_command import api_command
from aura.api_repository import make_api_call

# GET /instances

@api_command(help="List all instances in a tenant")
@click.option('--tenant-id', '-tid', help="The tenant from which you want to list instances")
def list(tenant_id):
    params={}
    if tenant_id is not None:
        params={"tenant_id": tenant_id}
    path = "/instances"
    
    return make_api_call("GET", path, params=params)
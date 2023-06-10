import click
from aura.api_command import api_command
from aura.api_repository import make_api_call

@api_command(help="Get details for a tenant")
@click.option('--tenant-id', '-tid', prompt=True, help="The ID of the tenant")
def get(tenant_id):
    path = f"/tenants/{tenant_id}"

    return make_api_call("GET", path)
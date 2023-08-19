import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.decorators import pass_config

# GET /instances


@api_command(help="List all instances in a tenant")
@click.option("--tenant-id", "-tid", help="The tenant from which you want to list instances")
@pass_config
def list(config, tenant_id):
    if tenant_id is None:
        tenant_id = config.get_option("default-tenant")

    params = {}
    if tenant_id is not None:
        #params = {"tenant_id": tenant_id}
        path = f"/instances?tenantId={tenant_id}"
    else:
        path = "/instances"
    return make_api_call("GET", path, params=params)

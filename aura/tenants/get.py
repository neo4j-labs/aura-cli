import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.decorators import pass_config
from aura.error_handler import NoTenantProvided

# GET /tenants/:tenantId

@api_command(help="Get details for a tenant")
@click.option('--tenant-id', '-id', help="The ID of the tenant")
@pass_config
def get(config, tenant_id):
    if tenant_id is None:
        tenant_id = config.get_option("default-tenant")
    if tenant_id is None:
        raise NoTenantProvided("You need to provide a tenant ID for this command. Either add an option or set a default tenant through the \`aura config\` command.")

    path = f"/tenants/{tenant_id}"

    return make_api_call("GET", path)
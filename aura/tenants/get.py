import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.config_repository import CLIConfig
from aura.decorators import pass_config


@api_command(name="get", help_text="Get details for a tenant", fixed_cmd_output="json")
@click.option("--tenant-id", "-id", help="The ID of the tenant")
@pass_config
def get_tenant(config: CLIConfig, tenant_id: str):
    """
    Get details of a tenant.

    Makes "GET /tenants/:tenantId" API request.

    fixed_cmd_output is set to json because its a nested object that can not be
    displayed in table or text.
    """

    if tenant_id is None:
        tenant_id = config.env["default_tenant"]
    if tenant_id is None:
        tenant_id = click.prompt("Tenant ID")

    path = f"/tenants/{tenant_id}"

    return make_api_call("GET", path)

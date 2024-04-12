import click

from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.config_repository import CLIConfig
from aura.decorators import pass_config


@api_command(
    name="get-metrics-integration", help_text="Get metrics integration endpoint for a tenant"
)
@click.option("--tenant-id", "-id", help="The ID of the tenant")
@pass_config
def get_tenant_metrics_integration_details(config: CLIConfig, tenant_id: str):
    """
    Get metrics integration endpoint of a tenant.

    Makes "GET /tenants/:tenantId/metrics-integration" API request.
    """

    if tenant_id is None:
        tenant_id = config.env["default_tenant"]
    if tenant_id is None:
        tenant_id = click.prompt("Tenant ID")

    path = f"/tenants/{tenant_id}/metrics-integration"

    return make_api_call("GET", path)

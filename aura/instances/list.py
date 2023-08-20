import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.config_repository import CLIConfig
from aura.decorators import pass_config


@api_command(name="list", help_text="List all instances in a tenant")
@click.option("--tenant-id", "-tid", help="The tenant from which you want to list instances")
@pass_config
def list_instances(config: CLIConfig, tenant_id: str):
    """
    List all instances.

    Optionally a tenantId query parameter can be provided to filter by instances by tenant.

    Makes "GET /instances" API request.
    """

    if tenant_id is None:
        tenant_id = config.get_option("default-tenant")

    if tenant_id is not None:
        path = f"/instances?tenantId={tenant_id}"
    else:
        path = "/instances"
    return make_api_call("GET", path)

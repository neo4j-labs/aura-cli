import click
from .get import get_tenant
from .list import list_tenants
from .get_metrics_integration import get_tenant_metrics_integration_details


@click.group(help="Get and list tenants")
def tenants():
    pass


tenants.add_command(get_tenant)
tenants.add_command(list_tenants)
tenants.add_command(get_tenant_metrics_integration_details)

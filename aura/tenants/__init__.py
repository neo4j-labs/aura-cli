import click
from .get import get_tenant
from .list import list_tenants


@click.group(help="Get and list tenants")
def tenants():
    pass


tenants.add_command(get_tenant)
tenants.add_command(list_tenants)

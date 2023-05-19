import click
from aura.instances import instances
from aura.credentials import credentials
from aura.snapshots import snapshots
from aura.tenants import tenants

@click.group()
def cli():
    pass


cli.add_command(credentials)
cli.add_command(instances)
cli.add_command(snapshots)
cli.add_command(tenants)

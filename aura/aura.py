import click
from aura.instances import instances
from aura.configure import configure
from aura.snapshots import snapshots
from aura.tenants import tenants

@click.group()
def cli():
    pass


cli.add_command(configure)
cli.add_command(instances)
cli.add_command(snapshots)
cli.add_command(tenants)

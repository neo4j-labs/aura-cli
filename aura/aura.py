import click
from aura.config_repository import CLIConfig
from aura.instances import instances
from aura.credentials import credentials
from aura.snapshots import snapshots
from aura.tenants import tenants

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = CLIConfig()


cli.add_command(credentials)
cli.add_command(instances)
cli.add_command(snapshots)
cli.add_command(tenants)

import click
from aura.config_repository import CLIConfig
from aura.instances import instances
from aura.credentials import credentials
from aura.snapshots import snapshots
from aura.tenants import tenants
from aura.config import config
from aura.version import __version__


@click.group()
@click.version_option(
    message=f"Aura CLI: version {__version__}, Aura API: version v1",
    package_name="aura-cli",
)
@click.pass_context
def cli(ctx):
    ctx.obj = CLIConfig()


cli.add_command(credentials)
cli.add_command(instances)
cli.add_command(snapshots)
cli.add_command(tenants)
cli.add_command(config)

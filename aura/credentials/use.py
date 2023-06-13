import click
from aura.config_repository import CLIConfig, use_credentials

@click.argument("name")
@click.command(help="Select which OAuth client credentials to use for authentication")
def use(name):
    config = CLIConfig()
    config.use_credentials(name)


    click.echo("")
    click.echo(f"Now using credentials {name}")
    
import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import handle_error


@click.argument("name")
@click.command(name="use", help="Select which OAuth client credentials to use for authentication")
@pass_config
def use_credentials(config: CLIConfig, name: str):
    """
    Use the speccified credentials
    """
    try:
        config.use_credentials(name)
    except Exception as exception:
        handle_error(exception)

    click.echo("")
    click.echo(f"Now using credentials {name}")

import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error
from aura.decorators import pass_config


@click.argument("name")
@click.command(name="delete", help="Delete OAuth client credentials")
@pass_config
def delete_credentials(config: CLIConfig, name: str):
    """
    Deletes the specified credentials
    """
    try:
        config.delete_credentials(name)
    except Exception as exception:
        handle_error(exception)

    click.echo("")
    click.echo(f"Credentials {name} successfully deleted")

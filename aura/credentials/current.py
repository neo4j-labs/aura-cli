import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error
from aura.decorators import pass_config


@click.command(name="current", help="Print the currently selected credentials")
@pass_config
def current_credentials(config: CLIConfig):
    """
    Print the credentials currently in use
    """
    try:
        name, creds = config.current_credentials()
    except Exception as exception:
        handle_error(exception)

    if name is None:
        return click.echo("No credentials have been selected.")

    client_id = creds["CLIENT_ID"]

    click.echo("Current credentials:")
    click.echo(f"Name:\t\t{name}")
    click.echo(f"Client ID:\t{client_id}")

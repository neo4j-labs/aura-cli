import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error

@click.command(help="Print the currently selected credentials")
def current():
    
    try:
        config = CLIConfig()
        name, creds = config.current_credentials()
    except Exception as e:
        handle_error(e)

    if name is None:
        return click.echo("No credentials have been selected.")
    
    client_id = creds["CLIENT_ID"]

    click.echo("Current credentials:")
    click.echo(f"Name:\t\t{name}")
    click.echo(f"Client ID:\t{client_id}")

    
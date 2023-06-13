import click
from aura.config_repository import CLIConfig, current_credentials

@click.command(help="Print the currently selected credentials")
def current():
    config = CLIConfig()
    name, creds = config.current_credentials()
    client_id = creds["CLIENT_ID"]

    if name is None:
        return click.echo("No credentials have been added yet.")

    click.echo("Current credentials:")
    click.echo(f"Name:\t\t{name}")
    click.echo(f"Client ID:\t{client_id}")

    
import click
from aura.config_repository import current_credentials

@click.command(help="Print the currently active credentials")
def current():
    name, client_id = current_credentials()

    if name is None:
        return click.echo("No credentials have been added yet.")

    click.echo("Current credentials:")
    click.echo(f"Name:\t\t{name}")
    click.echo(f"Client ID:\t{client_id}")

    
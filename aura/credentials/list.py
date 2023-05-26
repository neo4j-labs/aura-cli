import click
from aura.config_repository import list_credentials
from aura.format import print_text

@click.command(help="List all configured OAuth client credentials")
def list():
    credentials = list_credentials()

    if not credentials:
        return click.echo("No credentials have been added yet.")

    print_text(credentials)
    
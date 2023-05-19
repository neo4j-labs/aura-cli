import click
from aura.config_repository import list_credentials

@click.command(help="List all configured OAuth client credentials")
def list():
    credentials = list_credentials()

    if not credentials:
        return click.echo("No credentials have been added yet.")

    for cred in credentials:
        click.echo(f"Name: {cred[0]}\t\t Client ID: {cred[1]}")
    
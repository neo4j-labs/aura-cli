import click
from aura.config_repository import add_credentials

@click.option('--name', '-n', prompt=True, help="Name for the credentials")
@click.option('--client-id', '-id', prompt=True, help="The client ID")
@click.option('--client-secret', '-s', prompt=True, help="The client secret")
@click.command(help="Add new OAuth client credentials")
def add(name, client_id, client_secret):
    add_credentials(name, client_id, client_secret)

    click.echo("")
    click.echo(f"Credentials {name} successfully saved. Now using {name} as credentials.")
    
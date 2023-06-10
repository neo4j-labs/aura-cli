import click
from aura.config_repository import delete_credentials

@click.option('--name', '-n', prompt=True, help="Name of the credentials you want to delete")
@click.command(help="Delete OAuth client credentials")
def delete(name):
    delete_credentials(name)

    click.echo("")
    click.echo(f"Credentials {name} successfully deleted")
    
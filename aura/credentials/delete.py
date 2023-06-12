import click
from aura.config_repository import delete_credentials

@click.argument('name')
@click.command(help="Delete OAuth client credentials")
def delete(name):
    delete_credentials(name)

    click.echo("")
    click.echo(f"Credentials {name} successfully deleted")
    
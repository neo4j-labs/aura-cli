import click
from aura.config_repository import CLIConfig

@click.argument('name')
@click.command(help="Delete OAuth client credentials")
def delete(name):
    config = CLIConfig()
    config.delete_credentials(name)

    click.echo("")
    click.echo(f"Credentials {name} successfully deleted")
    
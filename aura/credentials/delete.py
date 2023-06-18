import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error

@click.argument('name')
@click.command(help="Delete OAuth client credentials")
def delete(name):

    try:
        config = CLIConfig()
        config.delete_credentials(name)
    except Exception as e:
        handle_error(e)


    click.echo("")
    click.echo(f"Credentials {name} successfully deleted")
    
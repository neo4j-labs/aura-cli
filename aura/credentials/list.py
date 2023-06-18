import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error
from aura.format import print_text

@click.command(help="List all configured OAuth client credentials")
def list():

    try:
        config = CLIConfig()
        credentials = config.list_credentials()
    except Exception as e:
        handle_error(e)

    if not credentials:
        return click.echo("No credentials have been added yet.")

    print_text(credentials)
    
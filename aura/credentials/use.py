import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error

@click.argument("name")
@click.command(help="Select which OAuth client credentials to use for authentication")
def use(name):

    try:
        config = CLIConfig()
        config.use_credentials(name)
    except Exception as e:
        handle_error(e)


    click.echo("")
    click.echo(f"Now using credentials {name}")
    
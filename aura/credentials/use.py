import click
from aura.decorators import pass_config
from aura.error_handler import handle_error


@click.argument("name")
@click.command(help="Select which OAuth client credentials to use for authentication")
@pass_config
def use(config, name):
    try:
        config.use_credentials(name)
    except Exception as e:
        handle_error(e)

    click.echo("")
    click.echo(f"Now using credentials {name}")

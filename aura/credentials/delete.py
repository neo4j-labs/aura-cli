import click
from aura.error_handler import handle_error
from aura.decorators import pass_config

@click.argument('name')
@click.command(help="Delete OAuth client credentials")
@pass_config
def delete(config, name):

    try:
        config.delete_credentials(name)
    except Exception as e:
        handle_error(e)


    click.echo("")
    click.echo(f"Credentials {name} successfully deleted")
    
import click
from aura.error_handler import handle_error
from aura.decorators import pass_config

@click.option('--name', '-n', help="Name for the credentials")
@click.option('--client-id', '-id', help="The client ID")
@click.option('--client-secret', '-s', help="The client secret")
@click.command(help="Add new OAuth client credentials")
@pass_config
def add(config, name, client_id, client_secret):
    if not name:
        name =  click.prompt('Credentials Name')
    if not client_id:
        client_id =  click.prompt('Client ID')
    if not client_secret:
        client_secret =  click.prompt('Client Secret')

    
    try:
        config.add_credentials(name, client_id, client_secret)
    except Exception as e:
        handle_error(e)

    click.echo("")
    click.echo(f"Credentials \"{name}\" successfully saved. Now using \"{name}\" as credentials.")
    
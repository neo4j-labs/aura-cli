import click
from aura.config_repository import CLIConfig

@click.option('--name', '-n', help="Name for the credentials")
@click.option('--client-id', '-id', help="The client ID")
@click.option('--client-secret', '-s', help="The client secret")
@click.command(help="Add new OAuth client credentials")
def add(name, client_id, client_secret):
    if not name:
        name =  click.prompt('Credentials Name:')
    if not client_id:
        client_id =  click.prompt('Client ID:')
    if not client_secret:
        client_secret =  click.prompt('Client Secret:')


    config = CLIConfig()
    config.add_credentials(name, client_id, client_secret)

    click.echo("")
    click.echo(f"Credentials {name} successfully saved. Now using {name} as credentials.")
    
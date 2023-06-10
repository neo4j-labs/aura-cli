import click
from aura.config_repository import use_credentials

@click.argument("name")
@click.command(help="Select which OAuth client credentials to use for authentication")
def use(name):
    use_credentials(name)


    click.echo("")
    click.echo(f"Now using credentials {name}")
    
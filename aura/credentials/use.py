import click
from aura.config_repository import use_credentials

@click.option('--name', '-n', prompt=True)
@click.command(help="Use specific OAuth client credentials")
def use(name):
    use_credentials(name)

    click.echo("")
    click.echo(f"Now using credentials {name}")
    
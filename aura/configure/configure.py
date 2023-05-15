import configparser
import click
from aura.repository import write_config

@click.option('--client-id', '-id', prompt=True)
@click.option('--client-secret', '-s', prompt=True)
@click.command()
def configure(client_id, client_secret):
    config = configparser.ConfigParser()
    config["AUTH"] = {}
    config["AUTH"]["CLIENT_ID"] = client_id
    config["AUTH"]["CLIENT_SECRET"] = client_secret
    
    write_config(config)

    click.echo("")
    click.echo("Credentials successfully saved")
    
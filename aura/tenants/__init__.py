import click
from .get import get
from .list import list

@click.group()
def tenants():
    pass

tenants.add_command(get)
tenants.add_command(list)
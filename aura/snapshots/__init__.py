import click
from .create import create 
from .list import list
from .restore import restore

@click.group()
def snapshots():
    pass

snapshots.add_command(create)
snapshots.add_command(list)
snapshots.add_command(restore)
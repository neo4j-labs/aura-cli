import click
from .create import create
from .list import list
from .restore import restore
from .get import get


@click.group(help="Manage instance snapshots")
def snapshots():
    pass


snapshots.add_command(create)
snapshots.add_command(list)
snapshots.add_command(restore)
snapshots.add_command(get)

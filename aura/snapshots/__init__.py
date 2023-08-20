import click
from .create import create_snapshot
from .list import list_snapshots
from .restore import restore_snapshot
from .get import get_snapshot


@click.group(help="Manage instance snapshots")
def snapshots():
    pass


snapshots.add_command(create_snapshot)
snapshots.add_command(list_snapshots)
snapshots.add_command(restore_snapshot)
snapshots.add_command(get_snapshot)

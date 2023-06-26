import click
from .set import set
from .unset import unset
from .get import get
from .list import list

@click.group(help="Manage different configurations and set default values\n\nValid options:\n\n\tdefault-tenant\n\n\tdefault-output")
def config():
    pass

config.add_command(set)
config.add_command(unset)
config.add_command(get)
config.add_command(list)

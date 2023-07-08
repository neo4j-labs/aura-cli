import click
from .set import set
from .unset import unset
from .get import get
from .list import list

help_text = """
Manage configurations and set default values

Valid config options:\n
    • default-tenant\n
    • default-output

Example usage:\n
aura config set default-tenant <my-tenant-id>\n
aura config unset default-output
"""

@click.group(help=help_text)
def config():
    pass

config.add_command(set)
config.add_command(unset)
config.add_command(get)
config.add_command(list)

import click
from .set import set_option
from .unset import unset_option
from .get import get_option
from .list import list_options

HELP_TEXT = """
Manage configurations and set default values

Valid config options:\n
    • default-tenant\n
    • default-output

Example usage:\n
aura config set default-tenant <my-tenant-id>\n
aura config unset default-output
"""


@click.group(help=HELP_TEXT)
def config():
    pass


config.add_command(set_option)
config.add_command(unset_option)
config.add_command(get_option)
config.add_command(list_options)

import click
from .set import set_option, VALID_OPTIONS_HELP_TEXT
from .unset import unset_option
from .get import get_option
from .list import list_options

HELP_TEXT = f"""
Manage configurations and set default values

{VALID_OPTIONS_HELP_TEXT}

Example usage:\n
aura config set default_tenant <my-tenant-id>\n
aura config unset output\n
aura config set save_logs true
"""


@click.group(help=HELP_TEXT)
def config():
    pass


config.add_command(set_option)
config.add_command(unset_option)
config.add_command(get_option)
config.add_command(list_options)

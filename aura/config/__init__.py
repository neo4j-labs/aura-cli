import click
from .set import set_option
from .unset import unset_option
from .get import get_option
from .list import list_options

HELP_TEXT = """
Manage configurations and set default values

Valid config options:\n
    • default_tenant\tSet a default tenant\n
    • output\t\tSet a default output format\n
    • auth_url\t\tChange the auth url\n
    • base_url\t\tChange the api base url\n
    • save_logs\t\tFlag if CLI logs are saved to a file\n
    • log_file_path\tPath to file where logs are saved to

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

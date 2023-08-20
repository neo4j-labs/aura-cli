import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import InvalidConfigOption, handle_error
from .valid_options import VALID_OPTIONS

HELP_TEXT = """
Print a config option value

Valid config options:\n
    • default-tenant\n
    • default-output

Example usage:\n
aura config get default-tenant\n
aura config get default-output
"""


@click.argument("name")
@click.command(name="get", help=HELP_TEXT)
@pass_config
def get_option(config: CLIConfig, name: str):
    """
    Print a config option
    """
    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(f"No config option {name} exists")

        value = config.get_option(name)
    except Exception as exception:
        handle_error(exception)

    if value is None:
        return print(f"No value for {name} set")

    print(f'Config option {name} is set to "{value}"')

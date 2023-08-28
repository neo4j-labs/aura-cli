import click
from aura.config_repository import CLIConfig
from aura.config.valid_options import VALID_OPTIONS
from aura.decorators import pass_config
from aura.error_handler import (
    InvalidConfigOption,
    InvalidConfigOptionValue,
    handle_error,
)

HELP_TEXT = """
Set a config option to a new value

Valid config options:\n
    • default-tenant\n
    • default-output

Example usage:\n
aura config set default-tenant my-tenant-id\n
aura config set default-output table
"""


@click.command(name="set", help=HELP_TEXT)
@click.argument("name")
@click.argument("value")
@pass_config
def set_option(config: CLIConfig, name: str, value: str):
    """
    Set a config option to specified value
    """
    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(name)
        if value is None:
            raise InvalidConfigOptionValue(name)

        config.set_option(name, value)
    except Exception as exception:
        handle_error(exception)

    print(f'Config option {name} set to "{value}"')

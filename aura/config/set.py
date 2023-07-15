import click
from .valid_options import VALID_OPTIONS
from aura.decorators import pass_config
from aura.error_handler import (
    InvalidConfigOption,
    InvalidConfigOptionValue,
    handle_error,
)

help_text = """
Set a config option to a new value

Valid config options:\n
    • default-tenant\n
    • default-output

Example usage:\n
aura config set default-tenant my-tenant-id\n
aura config set default-output table
"""


@click.command(help=help_text)
@click.argument("name")
@click.argument("value")
@pass_config
def set(config, name, value):
    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(f"No config option {name} exists")
        if value is None:
            raise InvalidConfigOptionValue(
                f"Please add a valid value for option {name}"
            )

        config.set_option(name, value)
    except Exception as e:
        handle_error(e)

    print(f'Config option {name} set to "{value}"')

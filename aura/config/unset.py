import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import InvalidConfigOption, handle_error
from .valid_options import VALID_OPTIONS

HELP_TEXT = """
Unset a config option value

Valid config options:\n
    • default-tenant\n
    • default-output

Example usage:\n
aura config unset default-tenant\n
aura config unset default-output
"""


@click.argument("name")
@click.command(name="unset", help=HELP_TEXT)
@pass_config
def unset_option(config: CLIConfig, name: str):
    """
    Delete a config value
    """
    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(name)

        config.unset_option(name)
    except Exception as exception:
        handle_error(exception)

    print(f"Config option {name} unset")

import click
from aura.config_repository import CLIConfig
from aura.config.valid_options import VALID_OPTIONS
from aura.decorators import pass_config
from aura.error_handler import (
    InvalidConfigOption,
    InvalidConfigOptionValue,
    handle_error,
)
from aura.logger import get_logger

HELP_TEXT = """
Set a config option to a new value

Valid config options:\n
    • default_tenant\n
    • output\n
    • auth_url\n
    • base_url


Example usage:\n
aura config set default_tenant my-tenant-id\n
aura config set output table
"""


@click.command(name="set", help=HELP_TEXT)
@click.argument("name")
@click.argument("value")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@pass_config
def set_option(config: CLIConfig, name: str, value: str, verbose: bool):
    """
    Set a config option to specified value
    """
    logger = get_logger("auracli")

    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(name)
        if value is None:
            raise InvalidConfigOptionValue(name)

        config.set_option(name, value)
    except Exception as exception:
        handle_error(exception)

    logger.info(f'Config option {name} set to "{value}"')
    if not config.env["VERBOSE"]:
        print(f'Config option {name} set to "{value}"')

    logger.debug("CLI command completed successfully.")

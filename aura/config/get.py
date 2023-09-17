import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import InvalidConfigOption, handle_error
from aura.logger import get_logger
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
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@pass_config
# pylint: disable=unused-argument
def get_option(config: CLIConfig, name: str, verbose: bool):
    """
    Print a config option
    """
    logger = get_logger()

    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(name)

        value = config.get_option(name)
    except Exception as exception:
        handle_error(exception)

    if value is None:
        logger.info(f"No value for {name} set")
        if not config.env["verbose"]:
            print(f"No value for {name} set")
    else:
        logger.info(f'Config option {name} is set to "{value}"')
        if not config.env["verbose"]:
            print(f'Config option {name} is set to "{value}"')

    logger.debug("CLI command completed successfully.")

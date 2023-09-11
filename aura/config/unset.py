import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import InvalidConfigOption, handle_error
from aura.logger import get_logger
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
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@click.command(name="unset", help=HELP_TEXT)
@pass_config
def unset_option(config: CLIConfig, name: str, verbose: bool):
    """
    Delete a config value
    """
    logger = get_logger("auracli")

    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(name)

        config.unset_option(name)
    except Exception as exception:
        handle_error(exception)

    logger.info(f"Config option {name} unset")
    if not config.env["verbose"]:
        print(f"Config option {name} unset")

    logger.debug("CLI command completed successfully.")

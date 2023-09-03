import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import handle_error
from aura.format import format_text_output
from aura.logger import get_logger

HELP_TEXT = """
List all configured config options

Example usage:\n
aura config list
"""


@click.command(name="list", help=HELP_TEXT)
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@pass_config
def list_options(config: CLIConfig, verbose: bool):
    """
    List all configured config options
    """
    logger = get_logger("auracli")

    try:
        values = config.list_options()
    except Exception as exception:
        handle_error(exception)

    if values is None or len(values) == 0:
        logger.info(f"No config options set.")
        if not not config.env["VERBOSE"]:
            print("No config options set.")
    else:
        logger.info(f"Config options: {values}")
        if not config.env["VERBOSE"]:
            out = format_text_output(values)
            print(out)

    logger.debug("CLI command completed successfully.")

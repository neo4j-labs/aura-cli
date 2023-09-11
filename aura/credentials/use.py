import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import handle_error
from aura.logger import get_logger


@click.argument("name")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@click.command(name="use", help="Select which OAuth client credentials to use for authentication")
@pass_config
def use_credentials(config: CLIConfig, name: str, verbose: bool):
    """
    Use the speccified credentials
    """
    logger = get_logger("auracli")

    try:
        config.use_credentials(name)
    except Exception as exception:
        handle_error(exception)

    logger.info(f"Now using credentials {name}")
    if not config.env["verbose"]:
        print(f"Now using credentials {name}")

    logger.debug("CLI command completed successfully.")

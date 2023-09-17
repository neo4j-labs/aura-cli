import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error
from aura.decorators import pass_config
from aura.logger import get_logger


@click.argument("name")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@click.command(name="delete", help="Delete OAuth client credentials")
@pass_config
# pylint: disable=unused-argument
def delete_credentials(config: CLIConfig, name: str, verbose: bool):
    """
    Deletes the specified credentials
    """
    logger = get_logger()

    try:
        config.delete_credentials(name)
    except Exception as exception:
        handle_error(exception)

    logger.info(f"Credentials {name} successfully deleted")
    if not config.env["verbose"]:
        print(f"Credentials {name} successfully deleted")

    logger.debug("CLI command completed successfully.")

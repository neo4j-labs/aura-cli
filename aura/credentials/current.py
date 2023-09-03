import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error
from aura.decorators import pass_config
from aura.logger import get_logger


@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@click.command(name="current", help="Print the currently selected credentials")
@pass_config
def current_credentials(config: CLIConfig, verbose: bool):
    """
    Print the credentials currently in use
    """
    logger = get_logger("auracli")

    try:
        name, creds = config.current_credentials()
    except Exception as exception:
        handle_error(exception)

    if name is None:
        logger.info("No credentials have been selected.")
        if not config.env["VERBOSE"]:
            print("No credentials have been selected.")
    else:
        client_id = creds["CLIENT_ID"]
        logger.info(f"Current credentials: Name={name} ClientId={client_id}")
        if not config.env["VERBOSE"]:
            print("Current credentials:")
            print(f"Name:\t\t{name}")
            print(f"Client ID:\t{client_id}")

    logger.debug("CLI command completed successfully.")

import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import handle_error
from aura.format import format_text_output
from aura.logger import get_logger


@click.command(name="list", help="List all configured OAuth client credentials")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@pass_config
# pylint: disable=unused-argument
def list_credentials(config: CLIConfig, verbose: bool):
    """
    List all configured credentials
    """
    logger = get_logger()

    try:
        credentials = config.list_credentials()
        current_creds, _ = config.current_credentials()
    except Exception as exception:
        handle_error(exception)

    if not credentials:
        logger.info("No credentials have been added yet.")
        if not config.env["verbose"]:
            print("No credentials have been added yet.")
    else:
        logger.info("Credentials: " + ", ".join([creds["Name"] for creds in credentials]))
        if not config.env["verbose"]:
            output = []
            for creds in credentials:
                if creds["Name"] == current_creds:
                    output.append({**creds, "Current": "   X   "})
                else:
                    output.append({**creds, "Current": ""})

            out = format_text_output(output)
            print(out)

    logger.debug("CLI command completed successfully.")

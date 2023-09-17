import click
from aura.config_repository import CLIConfig
from aura.error_handler import handle_error
from aura.decorators import pass_config
from aura.logger import get_logger


@click.option("--name", "-n", help="Name for the credentials")
@click.option("--client-id", "-id", help="The client ID")
@click.option("--client-secret", "-s", help="The client secret")
@click.option("--use", "-u", is_flag=True, default=False, help="Use the credentials")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
@click.command(name="add", help="Add new OAuth client credentials")
@pass_config
# pylint: disable=unused-argument
def add_credentials(
    config: CLIConfig, name: str, client_id: str, client_secret: str, use: bool, verbose: bool
):
    """
    Add a new set of credentials
    """
    logger = get_logger()

    if not name:
        name = click.prompt("Credentials Name")
    if not client_id:
        client_id = click.prompt("Client ID")
    if not client_secret:
        client_secret = click.prompt("Client Secret")

    try:
        config.add_credentials(name, client_id, client_secret, use)
    except Exception as exception:
        handle_error(exception)

    msg = f'Credentials "{name}" successfully saved.'
    if use:
        msg += f' Now using "{name}" as credentials.'

    logger.info(msg)
    if not config.env["verbose"]:
        print(msg)

    logger.debug("CLI command completed successfully.")

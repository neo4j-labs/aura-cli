import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.config_repository import CLIConfig
from aura.decorators import pass_config


@api_command(name="list", help_text="List all dataconnectors")
@pass_config
def list_dataapis(config: CLIConfig):
    """
    List all data connectors.

    Makes "GET /dataconnectors" API request.
    """

    path = "/data-connectors"

    return make_api_call("GET", path)

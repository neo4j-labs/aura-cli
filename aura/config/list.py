import click
from aura.config_repository import CLIConfig
from aura.decorators import pass_config
from aura.error_handler import handle_error
from aura.format import format_text_output

HELP_TEXT = """
List all configured config options

Example usage:\n
aura config list
"""


@click.command(name="list", help=HELP_TEXT)
@pass_config
def list_options(config: CLIConfig):
    """
    List all configured config options
    """
    try:
        values = config.list_options()
    except Exception as exception:
        handle_error(exception)

    if values is None or len(values) == 0:
        return print("No config options set.")

    out = format_text_output(values)
    print(out)

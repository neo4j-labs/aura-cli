import click
from aura.decorators import pass_config
from aura.error_handler import handle_error
from aura.format import format_text_output

help_text = """
List all configured config options

Example usage:\n
aura config list
"""

@click.command(help=help_text)
@pass_config
def list(config):
    try:
        values = config.list_options()
    except Exception as e:
        handle_error(e)

    if values is None or len(values) == 0:
        return print(f"No config options set.")

    format_text_output(values)
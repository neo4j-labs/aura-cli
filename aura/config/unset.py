import click
from aura.decorators import pass_config
from aura.error_handler import InvalidConfigOption, handle_error
from .valid_options import VALID_OPTIONS

help_text = """
Unset a config option value

Valid config options:\n
    • default-tenant\n
    • default-output

Example usage:\n
aura config unset default-tenant\n
aura config unset default-output
"""

@click.argument("name")
@click.command(help=help_text)
@pass_config
def unset(config, name):
    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(f"No config option {name} exists")
        
        config.unset_option(name)
    except Exception as e:
        handle_error(e)

    print(f"Config option {name} unset")
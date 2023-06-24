import click
from aura.decorators import pass_config
from aura.error_handler import InvalidConfigOption, handle_error
from .valid_options import VALID_OPTIONS

@click.argument("name")
@click.command(help="Unset a config option value")
@pass_config
def unset(config, name):
    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(f"No config option {name} exists")
        
        config.unset_option(name)
    except Exception as e:
        handle_error(e)

    print(f"Config option {name} unset")
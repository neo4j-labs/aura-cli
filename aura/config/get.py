import click
from aura.decorators import pass_config
from aura.error_handler import InvalidConfigOption, handle_error
from .valid_options import VALID_OPTIONS

@click.argument("name")
@click.command(help="Print a config option value")
@pass_config
def get(config, name):
    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(f"No config option {name} exists")
    
        value = config.get_option(name)
    except Exception as e:
        handle_error(e)

    if value is None:
        print(f"No value for option {name} set")

    print(f"Config option {name} is set to \"{value}\"")
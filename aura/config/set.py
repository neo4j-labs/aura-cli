import click
from .valid_options import VALID_OPTIONS
from aura.decorators import pass_config
from aura.error_handler import InvalidConfigOption, InvalidConfigOptionValue, handle_error

@click.command(help="Set a config option to a new value\n\nValid options:\n\n\tdefault-tenant\n\n\tdefault-output")
@click.argument("name")
@click.argument("value")
@pass_config
def set(config, name, value):
    try:
        if name not in VALID_OPTIONS:
            raise InvalidConfigOption(f"No config option {name} exists")
        if value is None:
            raise InvalidConfigOptionValue(f"Please add a valid value for option {name}")
    
        config.set_option(name, value)
    except Exception as e:
        handle_error(e)

    print(f"Config option {name} set to \"{value}\"")



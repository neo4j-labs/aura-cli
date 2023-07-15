import click
from aura.config_repository import CLIConfig

# Decorator that will allow commands to access the config objects, which gets
# loaded once and passed through the click context
pass_config = click.make_pass_decorator(CLIConfig)

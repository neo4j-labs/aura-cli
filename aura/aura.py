from functools import wraps
import click
from aura.config_repository import CLIConfig
from aura.instances import instances
from aura.credentials import credentials
from aura.logger import get_logger
from aura.snapshots import snapshots
from aura.tenants import tenants
from aura.config import config
from aura.dataapis import dataapis
from aura.version import __version__

CLI_VERSION_MESSAGE = f"Aura CLI: version {__version__}, Aura API: version v1"


@click.group()
@click.version_option(
    message=CLI_VERSION_MESSAGE,
    package_name="aura-cli",
)
@click.pass_context
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
# pylint: disable=unused-argument
def cli(ctx, verbose: bool):
    ctx.obj = CLIConfig()


cli.add_command(credentials)
cli.add_command(instances)
cli.add_command(snapshots)
cli.add_command(tenants)
cli.add_command(config)
cli.add_command(dataapis)


def log_usage_errors(func):
    @wraps(func)
    def log_decorator(*args, **kwargs):
        logger = get_logger()
        logger.debug("Error: " + str(args[0]))
        logger.debug("CLI usage error. Exiting with status code 1.")
        func(*args, **kwargs)

    return log_decorator


# Update Usage Error handler
click.exceptions.UsageError.show = log_usage_errors(click.exceptions.UsageError.show)

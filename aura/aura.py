import click
import sys
from aura.config_repository import CLIConfig
from aura.instances import instances
from aura.credentials import credentials
from aura.logger import setup_logger
from aura.snapshots import snapshots
from aura.tenants import tenants
from aura.config import config
from aura.version import __version__

CLI_VERSION_MESSAGE = f"Aura CLI: version {__version__}, Aura API: version v1"


@click.group()
@click.version_option(
    message=CLI_VERSION_MESSAGE,
    package_name="aura-cli",
)
@click.pass_context
@click.option("--verbose", "-v", is_flag=True, default=False, help="Print verbose output")
def cli(ctx, verbose):
    # The verbose flag is supposed to be global but click does not allow checking
    # all nested subcommands and options at this level. So we manually check if the
    # flag was set at any level.
    is_verbose = verbose or "--verbose" in sys.argv

    logger = setup_logger(is_verbose)
    logger.debug("CLI initiated. " + CLI_VERSION_MESSAGE)
    logger.debug("CLI command called: aura " + " ".join(sys.argv[1:]))

    ctx.obj = CLIConfig()
    # Set verbosity in config object
    ctx.obj.env["VERBOSE"] = is_verbose


cli.add_command(credentials)
cli.add_command(instances)
cli.add_command(snapshots)
cli.add_command(tenants)
cli.add_command(config)

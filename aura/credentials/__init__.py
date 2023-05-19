import click
from .add import add
from .use import use
from .list import list
from .delete import delete
from .current import current


@click.group(help="Configure OAuth credentials for the Aura API")
def credentials():
    pass

credentials.add_command(add)
credentials.add_command(use)
credentials.add_command(list)
credentials.add_command(delete)
credentials.add_command(current)
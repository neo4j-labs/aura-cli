import click
from .add import add
from .use import use
from .list import list
from .delete import delete
from .current import current

help_text = """
Configure and manage OAuth credentials

Example usage:\n
aura credentials add --name prod --client-id <id> --client-secret <secret>\n
aura credentials use\n
aura credentials list
"""

@click.group(help=help_text)
def credentials():
    pass

credentials.add_command(add)
credentials.add_command(use)
credentials.add_command(list)
credentials.add_command(delete)
credentials.add_command(current)
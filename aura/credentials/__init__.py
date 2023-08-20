import click
from .add import add_credentials
from .use import use_credentials
from .list import list_credentials
from .delete import delete_credentials
from .current import current_credentials

HELP_TEXT = """
Configure and manage OAuth credentials

Example usage:\n
aura credentials add --name prod --client-id <id> --client-secret <secret>\n
aura credentials use\n
aura credentials list
"""


@click.group(help=HELP_TEXT)
def credentials():
    pass


credentials.add_command(add_credentials)
credentials.add_command(use_credentials)
credentials.add_command(list_credentials)
credentials.add_command(delete_credentials)
credentials.add_command(current_credentials)

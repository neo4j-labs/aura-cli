import click
from .create import create_dataapi
from .list import list_dataapis
from .update import update_dataapi, update_dataapi_graphql_td
from .get import get_dataapi
from .delete import delete_dataapi

@click.group(help="Manage your Data APIs")
def dataapis():
    pass


dataconnectors.add_command(create_dataapi)
dataconnectors.add_command(list_dataapis)
dataconnectors.add_command(update_dataapi)
dataconnectors.add_command(get_dataapi)
dataconnectors.add_command(update_dataapi_graphql_td)
dataconnectors.add_command(delete_dataapi)



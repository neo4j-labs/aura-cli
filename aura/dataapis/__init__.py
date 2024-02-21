import click
from .create import create_dataapi
from .list import list_dataapis
from .update import update_dataapi, update_dataapi_graphql_td
from .get import get_dataapi
from .delete import delete_dataapi

@click.group(help="Manage your Data APIs")
def dataapis():
    pass


dataapis.add_command(create_dataapi)
dataapis.add_command(list_dataapis)
dataapis.add_command(update_dataapi)
dataapis.add_command(get_dataapi)
dataapis.add_command(update_dataapi_graphql_td)
dataapis.add_command(delete_dataapi)



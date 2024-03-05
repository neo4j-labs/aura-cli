import click
from .list import list_data_apis
from .get import get_data_api
from .delete import delete_data_api


@click.group(help="Manage instance data APIs")
def data_apis():
    pass


data_apis.add_command(list_data_apis)
data_apis.add_command(get_data_api)
data_apis.add_command(delete_data_api)

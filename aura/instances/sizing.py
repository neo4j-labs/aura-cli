import json
from typing import List
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.config_repository import CLIConfig
from aura.decorators import pass_config


# pylint: disable=redefined-builtin
@api_command(name="sizing", help_text="Estimate the size of an instance")
@click.option("--type", "-t", prompt=True, help="The instance type")
@click.option(
    "--node-count", "-n", prompt=True, help="The estimated node count", type=int
)
@click.option(
    "--relationship-count",
    "-r",
    prompt=True,
    help="The estimated relationship count",
    type=int,
)
@click.option(
    "--algorithm-categories",
    "-ac",
    help="The GDS algorithm categories to be used",
    multiple=True,
    default=[],
    type=str,
)
@pass_config
def size_instance(
    config: CLIConfig,
    type: str,
    node_count: int,
    relationship_count: int,
    algorithm_categories: List[str],
):
    """
    Estimates the size of an instance using the given options.

    Makes "POST /instances/sizing" API request.
    """
    path = "/instances/sizing"

    data = {
        "node_count": node_count,
        "relationship_count": relationship_count,
        "algorithm_categories": algorithm_categories,
        "instance_type": type,
    }

    return make_api_call("POST", path, data=json.dumps(data))

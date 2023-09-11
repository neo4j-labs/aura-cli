import json
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.config_repository import CLIConfig
from aura.decorators import pass_config


# pylint: disable=redefined-builtin
@api_command(name="create", help_text="Create a new instance")
@click.option("--version", "-v", default="5", help="The instance version")
@click.option("--type", "-t", prompt=True, help="The instance type")
@click.option("--cloud-provider", "-cp", prompt=True, help="The cloud provider for the instance")
@click.option("--region", "-r", prompt=True, help="The instance region")
@click.option("--memory", "-m", default="2", help="The instance memory size")
@click.option("--name", "-n", default="Instance01", help="The instance name")
@click.option(
    "--tenant-id", "-tid", help="The ID of the tenant where you want to create the instance"
)
@pass_config
def create_instance(
    config: CLIConfig,
    version: str,
    region: str,
    memory: str,
    name: str,
    type: str,
    tenant_id: str,
    cloud_provider: str,
):
    """
    Create a new instance with specified options.

    Makes "POST /instances" API request.
    """

    if tenant_id is None:
        tenant_id = config.env["default_tenant"]
    if tenant_id is None:
        tenant_id = click.prompt("Tenant ID")

    path = "/instances"

    data = {
        "version": version,
        "region": region,
        "memory": f"{memory}GB",
        "name": name,
        "type": type,
        "tenant_id": tenant_id,
        "cloud_provider": cloud_provider,
    }

    return make_api_call("POST", path, data=json.dumps(data))

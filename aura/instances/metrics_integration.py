import click
from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command(name="get-metrics-integration", help_text="Get metrics integration details for an instance")
@click.option("--instance-id", "-id", help="The instance ID")
def get_instance_metrics_integration_details(instance_id: str):
    """
    Get metrics integration details of an instance.

    Makes "GET /instances/:instanceId/metrics-integration" API request.
    """

    if instance_id is None:
        instance_id = click.prompt("Instance ID")

    path = f"/instances/{instance_id}/metrics-integration"

    return make_api_call("GET", path)

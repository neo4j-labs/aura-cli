import click
from aura.api_command import api_command
from aura.api_repository import make_api_call, make_api_call_and_wait_for_instance_status
from aura.util.get_instance_id import get_instance_id


@api_command(name="resume", help_text="Resume an instance")
@click.option("--instance-id", "-id", help="The instance ID")
@click.option("--name", "-n", help="The instance name")
@click.option(
    "--wait",
    is_flag=True,
    default=False,
    help="Wait until instance is resumed",
)
def resume_instance(instance_id: str, name: str, wait: bool):
    """
    Resume a paused instance.

    Makes "POST /instances/:instanceId/resume" API request.
    """

    instance_id = get_instance_id(instance_id, name)

    path = f"/instances/{instance_id}/resume"

    if wait:
        return make_api_call_and_wait_for_instance_status("POST", path, "running")
    else:
        return make_api_call("POST", path)

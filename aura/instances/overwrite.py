import json
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id


@api_command(name="overwrite", help_text="Overwrite an instance")
@click.option("--instance-id", "-id", help="The instance ID")
@click.option("--source-instance", "-s", prompt=True, help="The source instance ID")
@click.option("--source-snapshot", help="The ID of a snapshot used for overwriting")
@click.option("--name", "-n", help="The instance name")
def overwrite_instance(instance_id: str, source_instance: str, source_snapshot: str, name: str):
    """
    Overwrite an instnace.

    The source-instance option is required. A source-snapshot is optional.

    Makes a "POST /instances/:instanceId/overwrite" API request.
    """

    instance_id = get_instance_id(instance_id, name)

    data = {"source_instance_id": source_instance}
    if source_snapshot:
        data["source_snapshot_id"] = source_snapshot

    path = f"/instances/{instance_id}/overwrite"

    return make_api_call("POST", path, data=json.dumps(data))

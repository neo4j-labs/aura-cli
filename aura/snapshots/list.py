from datetime import datetime
import click
from aura.api_command import api_command
from aura.api_repository import make_api_call
from aura.util.get_instance_id import get_instance_id

@api_command
@click.option('--instance-id', '-id')
@click.option('--instance-name', '-n')
@click.option('--date', '-d', default=datetime.now().strftime("%Y-%m-%d"))
def list(instance_id, instance_name, date):
    instance_id = get_instance_id(instance_id, instance_name)

    params={"date": date}
    path = f"/instances/{instance_id}/snapshots"

    return make_api_call("GET", path, params=params)
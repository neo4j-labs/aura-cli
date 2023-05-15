from datetime import datetime
import click
from aura.api_command import api_command
from aura.repository import make_api_call

@api_command
@click.option('--instance_id', '-id', prompt=True)
@click.option('--date', '-d', default=datetime.now().strftime("%Y-%m-%d"))
def list(instance_id, date):
    params={"date": date}
    path = f"/instances/{instance_id}/snapshots"

    return make_api_call("GET", path, params=params)
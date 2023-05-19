import click
import json
from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command
@click.option('--version', '-v', default="5")
@click.option('--region', '-r', prompt=True) 
@click.option('--memory', '-m', default="2")
@click.option('--name', '-n', default="Instance01")
@click.option('--type', '-t', prompt=True)
@click.option('--tenant-id', '-tid', prompt=True)
def create(version, region, memory, name, type, tenant_id):
    path = "/instances"

    data = {"version": version, "region": region, "memory": f"{memory}GB", "name": name, "type": type, "tenant_id": tenant_id}
    
    return make_api_call("POST", path, data=json.dumps(data))
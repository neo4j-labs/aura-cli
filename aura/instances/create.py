import click
import json
from aura.api_command import api_command
from aura.api_repository import make_api_call


@api_command(help="Create a new instance")
@click.option('--version', '-v', default="5", help="The instance version")
@click.option('--region', '-r', prompt=True, help="The instance region") 
@click.option('--memory', '-m', default="2", help="The instance memory size")
@click.option('--name', '-n', default="Instance01", help="The instance name")
@click.option('--type', '-t', prompt=True, help="The instance type")
@click.option('--tenant-id', '-tid', prompt=True, help="The ID of the tenant where you want to create the instance")
def create(version, region, memory, name, type, tenant_id):
    path = "/instances"

    data = {"version": version, "region": region, "memory": f"{memory}GB", "name": name, "type": type, "tenant_id": tenant_id}
    
    return make_api_call("POST", path, data=json.dumps(data))
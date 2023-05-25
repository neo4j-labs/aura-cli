import click
from aura.api_repository import make_api_call

def get_instance_id(instance_id, instance_name):
    if instance_id is not None and instance_name is not None:
        raise click.UsageError("Only one of the options instance-id and instance-name should be provided")
    
    if instance_id is not None:
        return instance_id
    
    if instance_name is None:
        raise click.UsageError("You need to provide either an instance-id or an instance-name")
    
    try:
        instances = make_api_call("GET", "/instances")["data"]

        for instance in instances:
            if instance["name"] == instance_name:
                return instance["id"]
        return Exception(f"Error: No instance with name {instance_name} found")
    except:
        raise Exception("An error occurred")


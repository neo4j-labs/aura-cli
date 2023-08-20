from aura.api_repository import make_api_call
from aura.error_handler import (
    InstanceNameNotUnique,
    InstanceIDAndNameBothProvided,
    InstanceIDorNameMissing,
    InstanceNameNotFound,
)


def get_instance_id(instance_id, instance_name):
    """
    For all commands related to a database instance, either an ID or a name can be provided.
    This function checks if exaclty one of the 2 options was provided and if it was the instance name,
    it will try to find the ID from the name
    """
    if instance_id is not None and instance_name is not None:
        raise InstanceIDAndNameBothProvided(
            "Only one of the options instance-id and instance-name should be"
            " provided"
        )

    if instance_id is not None:
        return instance_id

    if instance_name is None:
        raise InstanceIDorNameMissing(
            "You need to provide either an instance-id or an instance-name"
        )

    response = make_api_call("GET", "/instances")

    instances = response.json()["data"]

    id = None
    for instance in instances:
        if instance["name"] == instance_name:
            if id is not None:
                raise InstanceNameNotUnique(
                    "There is more than one instance with the provided name."
                    " Please use the id instead."
                )
            id = instance["id"]

    if id is not None:
        return id

    raise InstanceNameNotFound(
        f"Error: No instance with name {instance_name} found"
    )

import click

from aura.instances.sizing import size_instance
from .create import create_instance
from .get import get_instance
from .list import list_instances
from .update import update_instance
from .delete import delete_instance
from .pause import pause_instance
from .resume import resume_instance
from .overwrite import overwrite_instance


@click.group(help="Manage your Aura instances")
def instances():
    pass


instances.add_command(create_instance)
instances.add_command(size_instance)
instances.add_command(get_instance)
instances.add_command(list_instances)
instances.add_command(update_instance)
instances.add_command(delete_instance)
instances.add_command(pause_instance)
instances.add_command(resume_instance)
instances.add_command(overwrite_instance)

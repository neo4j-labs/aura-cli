import click
from .create import create
from .get import get
from .list import list
from .update import update
from .delete import delete
from .pause import pause
from .resume import resume
from .overwrite import overwrite

@click.group()
def instances():
    pass

instances.add_command(create)
instances.add_command(get)
instances.add_command(list)
instances.add_command(update)
instances.add_command(delete)
instances.add_command(pause)
instances.add_command(resume)
instances.add_command(overwrite)
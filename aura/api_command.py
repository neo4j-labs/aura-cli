import click
from pprint import pprint
from functools import wraps
from aura.error_handler import handle_api_error

def api_command(func):
    @click.command()
    @click.option("--output", default="json", help='Set the output format of a command')
    @wraps(func)
    def wrapper(output, *args, **kwargs):
        try:
            api_response = func(*args, **kwargs)
            data = api_response["data"]
        except Exception as e:
            handle_api_error(e)
        else:
            if output == "json":
                pprint(data)
            else:
                # TODO add output formats
                click.echo(data)
            click.get_current_context().exit(code=0)
    return wrapper

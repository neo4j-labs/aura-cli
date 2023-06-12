import click
from pprint import pprint
from functools import wraps
from aura.error_handler import handle_api_error
from aura.format import print_table, print_text

def api_command(help):

    def api_command_decorator(func):
        @click.command(help=help)
        @click.option("--output", default="json", help='Set the output format of a command')
        @wraps(func)
        def wrapper(output, *args, **kwargs):
            try:
                api_response = func(*args, **kwargs)
                data = None
                if "data" in api_response:
                    data = api_response["data"]
            except Exception as e:
                handle_api_error(e)
            else:
                if not data:
                    print("Operation successful")
                elif output == "json":
                    pprint(data)
                elif output == "table":
                    print_table(data)
                elif output == "text":
                    print_text(data)
                else:
                    raise click.UsageError(f"Unsupported output format {output}")
                click.get_current_context().exit(code=0)
        return wrapper
    
    return api_command_decorator
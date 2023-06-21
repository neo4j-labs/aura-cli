import click
from pprint import pprint
from functools import wraps
from aura.error_handler import UnsupportedOutputFormat, handle_error
from aura.format import format_table_output, format_text_output

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
                handle_error(e)
            else:
                if data is None:
                    print("Operation successful")
                elif output == "json":
                    pprint(data)
                elif output == "table":
                    format_table_output(data)
                elif output == "text":
                    format_text_output(data)
                else:
                    raise UnsupportedOutputFormat(f"Unsupported output format {output}")
                click.get_current_context().exit(code=0)
        return wrapper
    
    return api_command_decorator
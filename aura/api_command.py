import click
from pprint import pprint
from functools import wraps
from aura.error_handler import UnsupportedOutputFormat, handle_error
from aura.format import format_table_output, format_text_output

def api_command(help):

    def api_command_decorator(func):
        @click.command(help=help)
        @click.option("--output", help='Set the output format of a command')
        @click.option("--include", "-i", is_flag=True, default=False, help='Display Headers of the API response')
        @wraps(func)
        def wrapper(output, include, *args, **kwargs):
            try:
                api_response = func(*args, **kwargs)

                response_data = api_response.json()
                data = None
                if "data" in response_data:
                    data = response_data["data"]
            except Exception as e:
                handle_error(e)
            else:
                if include:
                    print(api_response.headers, "\n")

                ctx = click.get_current_context()
                config = ctx.obj
                output_format = output or config.get_option("default-output") or "json"
                
                if data is None:
                    print("Operation successful")
                elif output_format == "json":
                    pprint(data)
                elif output_format == "table":
                    format_table_output(data)
                elif output_format == "text":
                    format_text_output(data)
                else:
                    raise UnsupportedOutputFormat(f"Unsupported output format {output_format}")
                click.get_current_context().exit(code=0)
        return wrapper
    
    return api_command_decorator
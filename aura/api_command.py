import click
from requests.exceptions import *
from pprint import pprint
from functools import wraps

def api_command(func):
    @click.command()
    @click.option("--pretty", is_flag=True, help='Pretty-print the JSON output')
    @wraps(func)
    def wrapper(pretty, *args, **kwargs):
        try:
            api_response = func(*args, **kwargs)
            data = api_response["data"]
        except Exception as e:
            handle_api_error(e)
        else:
            if pretty:
                pprint(data)
            else:
                click.echo(data)
            click.get_current_context().exit(code=0)
    return wrapper


def handle_api_error(exception):
    if isinstance(exception, HTTPError):
        try:
            error_data = exception.response.json()
            error_message = error_data.get('message', 'Unknown error')
        except ValueError:
            error_message = f"Unknown error (status code {exception.response.status_code})"
    elif isinstance(exception,  Timeout):
        error_message = "Request timed out"
    elif isinstance(exception, ConnectionError):
        error_message = "Connection error"
    else:
        error_message = "An unexpected error occurred"

    click.echo(f"Error: {error_message}", err=True)
    click.get_current_context().exit(code=1)
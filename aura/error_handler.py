from requests.exceptions import *
import click

def handle_api_error(exception):
    #TODO remove and replace with better error message
    print(exception)

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
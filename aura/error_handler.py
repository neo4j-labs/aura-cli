from requests.exceptions import *
import click

def handle_error(exception):

    if isinstance(exception, HTTPError):
        try:
            error_data = exception.response.json()
            error_message = "Unknown Error"
            if "error" in error_data:
                error_message = error_data["error"]
            elif "errors" in error_data:
                error_message = "\n".join([e["message"] for e in error_data["errors"]])
            elif exception.response.status_code == 404:
                error_message = str(exception)
        except ValueError:
            error_message = f"Unknown error (status code {exception.response.status_code})"
    elif isinstance(exception, ClientError):
        error_message = exception.message
    elif isinstance(exception,  Timeout):
        error_message = "Request timed out"
    elif isinstance(exception, ConnectionError):
        error_message = "Connection error"
    else:
        error_message = "An unexpected error occurred"

    click.echo(f"Error: {error_message}", err=True)
    click.get_current_context().exit(code=1)

class ClientError(Exception):
    def __init__(self, message):
        self.message = message

class InstanceNameNotFound(ClientError):
    pass

class InstanceIDAndNameBothProvided(ClientError):
    pass

class InstanceIDorNameMissing(ClientError):
    pass

class NoCredentialsConfigured(ClientError):
    pass

class CredentialsNotFound(ClientError):
    pass

class InvalidConfigFile(ClientError):
    pass

class CredentialsAlreadyExist(ClientError):
    pass

class UnsupportedOutputFormat(ClientError):
    pass

class DatabaseNameNotUnique(ClientError):
    pass

class InvalidConfigOption(ClientError):
    pass

class InvalidConfigOptionValue(ClientError):
    pass

class NoTenantProvided(ClientError):
    pass
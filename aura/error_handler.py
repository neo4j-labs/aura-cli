"""This module defines the error_handler function and a set of custom exceptions"""
from requests.exceptions import HTTPError, Timeout, ConnectionError as ConnError
import click


def handle_error(exception: Exception):
    """
    Handle exceptions by providing a user-friendly error message.

    Parameters:
    - exception (Exception): The exception instance to be handled.

    Output:
    Prints an appropriate error message based on the exception type.
    """

    if isinstance(exception, HTTPError):
        try:
            error_data = exception.response.json()
            error_message = "Unknown Error"

            # Most errors returned by the API will have a error/errors field with the error message
            if "error" in error_data:
                error_message = error_data["error"]
            elif "errors" in error_data:
                error_message = "\n".join(
                    [e["message"] for e in error_data["errors"]]
                )
            elif exception.response.status_code == 404:
                error_message = str(exception)
        except ValueError:
            error_message = (
                f"Unknown error (status code {exception.response.status_code})"
            )

    elif isinstance(exception, ClientError):
        error_message = exception.message
    elif isinstance(exception, Timeout):
        error_message = "Request timed out"
    elif isinstance(exception, ConnError):
        error_message = "Connection error"
    else:
        error_message = "An unexpected error occurred"

    click.echo(f"Error: {error_message}", err=True)
    click.get_current_context().exit(code=1)


class ClientError(Exception):
    """Base exception for client-related errors."""

    def __init__(self, message):
        self.message = message


class InstanceNameNotFound(ClientError):
    """Exception raised when no instance with given name is found"""


class InstanceIDAndNameBothProvided(ClientError):
    """Exception raised when providing both instance ID and name in a command"""


class InstanceIDorNameMissing(ClientError):
    """
    Exception raised when providing neither instance ID nor name
    in a command where either is required
    """


class NoCredentialsConfigured(ClientError):
    """Exception raised when calling an API command and no credentials were configured"""


class CredentialsNotFound(ClientError):
    """Exception raised when selecting credentials that were not configured"""


class InvalidConfigFile(ClientError):
    """Exception raised when the config file contains validation errors"""


class CredentialsAlreadyExist(ClientError):
    """Exception raised when adding credentials with a name that already exists"""


class UnsupportedOutputFormat(ClientError):
    """Exception raised when providing an unsupported output format"""


class InstanceNameNotUnique(ClientError):
    """
    Exception raised when using when providing an instance name in a command but there are
    multiple instances with that name. In this case the instance ID must be used
    """


class InvalidConfigOption(ClientError):
    """Exception raised when setting a non-existend config option"""


class InvalidConfigOptionValue(ClientError):
    """Exception raised when setting a config option with an invalid value"""


class NoTenantProvided(ClientError):
    """Exception raised when a tenant is not provided in a command where it is required"""

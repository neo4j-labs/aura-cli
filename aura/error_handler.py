"""This module defines the error_handler function and a set of custom exceptions"""
from requests.exceptions import HTTPError, Timeout, ConnectionError as ConnError
import click

from aura.logger import get_logger


def handle_error(exception: Exception):
    """
    Handle exceptions by providing a user-friendly error message.

    Parameters:
    - exception (Exception): The exception instance to be handled.

    Output:
    Prints an appropriate error message based on the exception type.
    """
    logger = get_logger()

    if isinstance(exception, HTTPError):
        try:
            error_data = exception.response.json()
            error_message = "Unknown Error"

            if exception.response.status_code in [403, 404]:
                error_message = str(exception)
            # Most errors returned by the API will have a error/errors field with the error message
            elif "error" in error_data:
                error_message = error_data["error"]
            elif "errors" in error_data:
                error_message = "\n".join([e["message"] for e in error_data["errors"]])
        except ValueError:
            error_message = f"Unknown error (status code {exception.response.status_code})"

    elif isinstance(exception, ClientError):
        error_message = exception.message
    elif isinstance(exception, Timeout):
        error_message = "Request timed out"
    elif isinstance(exception, ConnError):
        error_message = "Connection error"
    else:
        error_message = "An unexpected error occurred"

    ctx = click.get_current_context()
    config = ctx.obj

    if config.env.get("VERBOSE"):
        logger.warning(f"{error_message}")
        logger.warning("Exiting CLI with exit code 1.")
    else:
        click.echo(f"Error: {error_message}", err=True)

    click.get_current_context().exit(code=1)


class ClientError(Exception):
    """Base exception for client-related errors."""

    def __init__(self, message):
        self.message = message


class InstanceNameNotFound(ClientError):
    """Exception raised when no instance with given name is found"""

    def __init__(self, instance_name):
        message = f"No instance with name {instance_name} found"
        super().__init__(message)


class InstanceIDAndNameBothProvided(ClientError):
    """Exception raised when providing both instance ID and name in a command"""

    def __init__(self):
        super().__init__("Only one of the options instance-id and instance-name should be provided")


class InstanceIDorNameMissing(ClientError):
    """
    Exception raised when providing neither instance ID nor name
    in a command where either is required
    """

    def __init__(self):
        super().__init__("You need to provide either an instance-id or an instance-name")


class NoCredentialsConfigured(ClientError):
    """Exception raised when calling an API command and no credentials were configured"""

    def __init__(self):
        super().__init__(
            "No credentials are configured. Either add new credentials or export environment"
            " variables."
        )


class CredentialsNotFound(ClientError):
    """Exception raised when selecting credentials that were not configured"""

    def __init__(self, name):
        super().__init__(f"Credentials {name} not found")


class InvalidConfigFile(ClientError):
    """Exception raised when the config file contains validation errors"""

    def __init__(self):
        super().__init__("Invalid config file")


class CredentialsAlreadyExist(ClientError):
    """Exception raised when adding credentials with a name that already exists"""

    def __init__(self, name):
        super().__init__(f"Credentials with name {name} already exist.")


class UnsupportedOutputFormat(ClientError):
    """Exception raised when providing an unsupported output format"""

    def __init__(self, output_format):
        super().__init__(f"Unsupported output format {output_format}")


class InstanceNameNotUnique(ClientError):
    """
    Exception raised when using when providing an instance name in a command but there are
    multiple instances with that name. In this case the instance ID must be used
    """

    def __init__(self):
        super().__init__(
            "There is more than one instance with the provided name. Please use the id instead."
        )


class InvalidConfigOption(ClientError):
    """Exception raised when setting a non-existend config option"""

    def __init__(self, option):
        super().__init__(f"No config option {option} exists")


class InvalidConfigOptionValue(ClientError):
    """Exception raised when setting a config option with an invalid value"""

    def __init__(self, option):
        super().__init__(f"Please add a valid value for option {option}")


class UnsupportedConfigFileVersion(ClientError):
    """Exception raised when version of the config file is too outdated"""

    def __init__(self, path):
        super().__init__(
            "The version of your CLI config file is not supported. Please delete the file at:"
            f" {path}"
        )

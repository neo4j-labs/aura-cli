from unittest.mock import patch, Mock

import pytest
from requests.exceptions import Timeout, ConnectionError, HTTPError

from aura.error_handler import (
    handle_error,
    InstanceNameNotFound,
    InstanceIDAndNameBothProvided,
    InstanceIDorNameMissing,
    NoCredentialsConfigured,
    CredentialsNotFound,
    InvalidConfigFile,
    CredentialsAlreadyExist,
    InstanceNameNotUnique,
    InvalidConfigOption,
    InvalidConfigOptionValue,
    UnsupportedConfigFileVersion,
)


@pytest.fixture
def mock_echo():
    with patch("click.echo") as m:
        yield m


@pytest.fixture
def mock_get_context():
    with patch("click.get_current_context") as m:
        m.return_value.exit = Mock()
        yield m


class MockHTTPError(HTTPError):
    def __init__(self, json_return_value=None, status_code=None):
        super().__init__()
        self.response = Mock()
        self.response.json.return_value = json_return_value
        self.response.status_code = status_code


@pytest.mark.parametrize(
    "error, expected_message",
    [
        (Timeout(), "Error: Request timed out"),
        (ConnectionError(), "Error: Connection error"),
        (InstanceNameNotFound("test-instance"), "Error: No instance with name test-instance found"),
        (
            InstanceIDAndNameBothProvided(),
            "Error: Only one of the options instance-id and instance-name should be provided",
        ),
        (
            InstanceIDorNameMissing(),
            "Error: You need to provide either an instance-id or an instance-name",
        ),
        (
            NoCredentialsConfigured(),
            (
                "Error: No credentials are configured. Either add new credentials or export"
                " environment variables."
            ),
        ),
        (CredentialsNotFound("test"), "Error: Credentials test not found"),
        (InvalidConfigFile(), "Error: Invalid config file"),
        (CredentialsAlreadyExist("test"), "Error: Credentials with name test already exist."),
        (
            InstanceNameNotUnique(),
            (
                "Error: There is more than one instance with the provided name. Please use the id"
                " instead."
            ),
        ),
        (InvalidConfigOption("test"), "Error: No config option test exists"),
        (InvalidConfigOptionValue("test"), "Error: Please add a valid value for option test"),
        (
            MockHTTPError(status_code=400, json_return_value={"error": "Some error happened"}),
            "Error: Some error happened",
        ),
        (
            MockHTTPError(
                status_code=400,
                json_return_value={
                    "errors": [{"message": "First error"}, {"message": "Second error"}]
                },
            ),
            "Error: First error\nSecond error",
        ),
        (
            UnsupportedConfigFileVersion("test-path/config.json"),
            (
                "Error: The version of your CLI config file is not supported. Please delete the"
                " file at: test-path/config.json"
            ),
        ),
    ],
)
def test_handle_error(error, expected_message, mock_echo, mock_get_context):
    handle_error(error)

    mock_echo.assert_called_once_with(expected_message, err=True)
    mock_get_context.return_value.exit.assert_called_once_with(code=1)

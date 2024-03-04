import json
from aura.config_repository import CLIConfig
import pytest
from unittest.mock import MagicMock, patch, Mock


def mock_headers():
    return {"Content-Type": "application/json", "Authorization": "Bearer dummy-token"}


@pytest.fixture(autouse=True)
def get_headers():
    with patch("aura.api_repository.get_headers", new=mock_headers):
        yield


@pytest.fixture()
def api_request():
    with patch("requests.request", new_callable=Mock()) as mocked_request:
        yield mocked_request


# Utility function to verify the command output is printed correctly
def printed_data(data):
    return json.dumps(data, indent=2) + "\n"


@pytest.fixture()
def mock_config():
    mock_config = MagicMock(spec=CLIConfig)
    mock_config.env = {
        "verbose": False,
        "output": "json",
        "default_tenant": None,
        "auth_url": "https://api.neo4j.io/oauth/token",
        "base_url": "https://api.neo4j.io/v1",
        "save_logs": False,
        "log_file_path": None,
    }
    mock_config.get_option.return_value = None
    yield mock_config


@pytest.fixture()
def mock_data_api_config():
    mock_config = MagicMock(spec=CLIConfig)
    mock_config.env = {
        "verbose": False,
        "output": "json",
        "default_tenant": None,
        "auth_url": "https://api-staging.neo4j.io/oauth/token",
        "base_url": "https://graphql-api-staging.neo4j.io/v1",
        "save_logs": False,
        "log_file_path": None,
    }
    mock_config.get_option.return_value = None
    yield mock_config


@pytest.fixture()
def mock_version():
    with patch("aura.api_repository.__version__", new="1.0.0") as mocked_version:
        yield mocked_version

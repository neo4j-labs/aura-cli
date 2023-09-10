import json
from unittest.mock import patch, mock_open, MagicMock
from aura.error_handler import CredentialsNotFound
import pytest

from aura.config_repository import CLIConfig

mock_env = {
    "verbose": False,
    "output": "json",
    "default_tenant": None,
    "auth_url": "https://api.neo4j.io/oauth/token",
    "base_url": "https://api.neo4j.io/v1",
    "save_logs": False,
    "log_file_path": None,
}


@pytest.fixture
def mock_cli_config():
    with patch.object(CLIConfig, "load_config", return_value=None), patch.object(
        CLIConfig, "load_env", return_value=mock_env
    ):
        cli_config = CLIConfig()
        yield cli_config


def test_initialization_load_default_config():
    with patch("os.path.expanduser") as mock_expanduser, patch(
        "builtins.open", mock_open()
    ) as mock_file, patch.object(CLIConfig, "write_config") as mock_write_config, patch.object(
        CLIConfig, "load_env", return_value=mock_env
    ), patch(
        "aura.config_repository.setup_logger", return_value=MagicMock()
    ):
        mock_expanduser.return_value = "/mocked/path"
        mock_file.side_effect = FileNotFoundError()
        mock_write_config.return_value = CLIConfig.DEFAULT_CONFIG

        cli_config = CLIConfig()

        mock_write_config.assert_called_once_with(CLIConfig.DEFAULT_CONFIG)
        assert cli_config.config == CLIConfig.DEFAULT_CONFIG


def test_load_valid_config():
    valid_config = {
        "VERSION": "1.0.0",
        "AUTH": {
            "CREDENTIALS": {
                "example": {"CLIENT_ID": "example_id", "CLIENT_SECRET": "example_secret"}
            },
            "ACTIVE": "example",
        },
        "OPTIONS": {},
    }

    with patch("os.path.expanduser") as mock_expanduser, patch(
        "builtins.open", mock_open(read_data=json.dumps(valid_config))
    ) as mock_file, patch.object(CLIConfig, "load_env", return_value=mock_env), patch(
        "aura.config_repository.setup_logger", return_value=MagicMock()
    ):
        mock_expanduser.return_value = "/mocked/path"

        cli_config = CLIConfig()

        assert cli_config.config == valid_config


def test_add_credentials(mock_cli_config):
    initial_config = {
        "VERSION": "1.0.0",
        "AUTH": {"CREDENTIALS": {}, "ACTIVE": None},
        "OPTIONS": {},
    }

    with patch.object(CLIConfig, "write_config", return_value=None) as mock_write_config, patch(
        "aura.config_repository.delete_token_file"
    ) as mock_delete_token:
        mock_cli_config.config = initial_config

        mock_cli_config.add_credentials("test_name", "test_id", "test_secret", True)

        expected_config = {
            "VERSION": "1.0.0",
            "AUTH": {
                "CREDENTIALS": {
                    "test_name": {"CLIENT_ID": "test_id", "CLIENT_SECRET": "test_secret"}
                },
                "ACTIVE": "test_name",
            },
            "OPTIONS": {},
        }
        mock_write_config.assert_called_once_with(expected_config)
        mock_delete_token.assert_called_once()
        assert mock_cli_config.config == expected_config


def test_list_credentials(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {
            "CREDENTIALS": {
                "example1": {"CLIENT_ID": "example_id_1", "CLIENT_SECRET": "example_secret_1"},
                "example2": {"CLIENT_ID": "example_id_2", "CLIENT_SECRET": "example_secret_2"},
            },
            "ACTIVE": "example1",
        },
        "OPTIONS": {},
    }

    result = mock_cli_config.list_credentials()
    expected = [
        {"Name": "example1", "ClientId": "example_id_1"},
        {"Name": "example2", "ClientId": "example_id_2"},
    ]
    assert result == expected


def test_current_credentials(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {
            "CREDENTIALS": {
                "example1": {"CLIENT_ID": "example_id_1", "CLIENT_SECRET": "example_secret_1"},
                "example2": {"CLIENT_ID": "example_id_2", "CLIENT_SECRET": "example_secret_2"},
            },
            "ACTIVE": "example1",
        },
        "OPTIONS": {},
    }

    name, credentials = mock_cli_config.current_credentials()
    assert name == "example1"
    assert credentials == {"CLIENT_ID": "example_id_1", "CLIENT_SECRET": "example_secret_1"}


def test_current_credentials_none(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {
            "CREDENTIALS": {},
            "ACTIVE": None,
        },
        "OPTIONS": {},
    }

    name, credentials = mock_cli_config.current_credentials()
    assert name is None
    assert credentials is None


def test_delete_credentials(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {
            "CREDENTIALS": {
                "example1": {"CLIENT_ID": "example_id_1", "CLIENT_SECRET": "example_secret_1"},
                "example2": {"CLIENT_ID": "example_id_2", "CLIENT_SECRET": "example_secret_2"},
            },
            "ACTIVE": "example1",
        },
        "OPTIONS": {},
    }

    with patch.object(CLIConfig, "write_config", return_value=None) as mock_write_config, patch(
        "aura.config_repository.delete_token_file"
    ) as mock_delete_token:
        mock_cli_config.delete_credentials("example1")

        expected_config = {
            "VERSION": "1.0",
            "AUTH": {
                "CREDENTIALS": {
                    "example2": {"CLIENT_ID": "example_id_2", "CLIENT_SECRET": "example_secret_2"}
                },
                "ACTIVE": None,
            },
            "OPTIONS": {},
        }

        mock_write_config.assert_called_once_with(expected_config)
        mock_delete_token.assert_called_once()


def test_delete_credentials_not_found(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {
            "CREDENTIALS": {},
            "ACTIVE": None,
        },
        "OPTIONS": {},
    }

    with pytest.raises(CredentialsNotFound):
        mock_cli_config.delete_credentials("test")


def test_use_credentials(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {
            "CREDENTIALS": {
                "example1": {"CLIENT_ID": "example_id_1", "CLIENT_SECRET": "example_secret_1"},
                "example2": {"CLIENT_ID": "example_id_2", "CLIENT_SECRET": "example_secret_2"},
            },
            "ACTIVE": "example1",
        },
        "OPTIONS": {},
    }

    with patch.object(CLIConfig, "write_config", return_value=None) as mock_write_config, patch(
        "aura.config_repository.delete_token_file"
    ) as mock_delete_token:
        mock_cli_config.use_credentials("example2")

        expected_config = {
            "VERSION": "1.0",
            "AUTH": {
                "CREDENTIALS": {
                    "example1": {"CLIENT_ID": "example_id_1", "CLIENT_SECRET": "example_secret_1"},
                    "example2": {"CLIENT_ID": "example_id_2", "CLIENT_SECRET": "example_secret_2"},
                },
                "ACTIVE": "example2",
            },
            "OPTIONS": {},
        }

        mock_write_config.assert_called_once_with(expected_config)
        mock_delete_token.assert_called_once()


def test_use_credentials_not_found(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {
            "CREDENTIALS": {},
            "ACTIVE": None,
        },
        "OPTIONS": {},
    }

    with pytest.raises(CredentialsNotFound):
        mock_cli_config.use_credentials("test")


def test_set_option(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {"CREDENTIALS": {}, "ACTIVE": None},
        "OPTIONS": {},
    }

    with patch.object(mock_cli_config, "write_config", return_value=None) as mock_write:
        mock_cli_config.set_option("default-output", "table")

        assert mock_cli_config.config["OPTIONS"]["default-output"] == "table"
        mock_write.assert_called_once()


def test_unset_option(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {"CREDENTIALS": {}, "ACTIVE": None},
        "OPTIONS": {"default-output": "table"},
    }

    with patch.object(mock_cli_config, "write_config", return_value=None) as mock_write:
        mock_cli_config.unset_option("default-output")

        assert "default-output" not in mock_cli_config.config["OPTIONS"]
        mock_write.assert_called_once()


def test_get_option(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {"CREDENTIALS": {}, "ACTIVE": None},
        "OPTIONS": {"default-output": "text"},
    }

    assert mock_cli_config.get_option("default-output") == "text"


def test_list_options(mock_cli_config):
    mock_cli_config.config = {
        "VERSION": "1.0",
        "AUTH": {"CREDENTIALS": {}, "ACTIVE": None},
        "OPTIONS": {"default-output": "text", "default-tenant": "my-tenant-123"},
    }

    assert mock_cli_config.list_options() == [
        {"Option": "default-output", "Value": "text"},
        {"Option": "default-tenant", "Value": "my-tenant-123"},
    ]


def test_validate_config_valid(mock_cli_config):
    valid_config = {
        "VERSION": "1.0.0",
        "AUTH": {
            "CREDENTIALS": {
                "user1": {"CLIENT_ID": "client_id_1", "CLIENT_SECRET": "client_secret_1"}
            },
            "ACTIVE": "user1",
        },
        "OPTIONS": {"option1": "value1"},
    }

    mock_cli_config.validate_config(valid_config)

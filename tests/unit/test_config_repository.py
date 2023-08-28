import json
from unittest.mock import patch, mock_open, MagicMock
import pytest

from aura.config_repository import CLIConfig


def test_initialization_load_default_config():
    with patch("os.path.expanduser") as mock_expanduser, patch(
        "builtins.open", mock_open()
    ) as mock_file, patch.object(CLIConfig, "write_config") as mock_write_config:
        mock_expanduser.return_value = "/mocked/path"
        mock_file.side_effect = FileNotFoundError()
        mock_write_config.return_value = CLIConfig.DEFAULT_CONFIG

        cli_config = CLIConfig()

        mock_write_config.assert_called_once_with(CLIConfig.DEFAULT_CONFIG)
        assert cli_config.config == CLIConfig.DEFAULT_CONFIG


def test_load_valid_config():
    valid_config = {
        "AUTH": {
            "CREDENTIALS": {
                "example": {"CLIENT_ID": "example_id", "CLIENT_SECRET": "example_secret"}
            },
            "ACTIVE": "example",
        },
        "DEFAULTS": {},
    }

    with patch("os.path.expanduser") as mock_expanduser, patch(
        "builtins.open", mock_open(read_data=json.dumps(valid_config))
    ) as mock_file:
        mock_expanduser.return_value = "/mocked/path"

        cli_config = CLIConfig()

        assert cli_config.config == valid_config


def test_write_config():
    pass  # TODO


def test_add_credentials():
    initial_config = {"AUTH": {"CREDENTIALS": {}, "ACTIVE": None}, "DEFAULTS": {}}

    with patch.object(CLIConfig, "write_config", return_value=None) as mock_write_config, patch(
        "aura.config_repository.delete_token_file"
    ) as mock_delete_token:
        cli_config = CLIConfig()
        cli_config.config = initial_config

        cli_config.add_credentials("test_name", "test_id", "test_secret")

        expected_config = {
            "AUTH": {
                "CREDENTIALS": {
                    "test_name": {"CLIENT_ID": "test_id", "CLIENT_SECRET": "test_secret"}
                },
                "ACTIVE": "test_name",
            },
            "DEFAULTS": {},
        }
        mock_write_config.assert_called_once_with(expected_config)
        mock_delete_token.assert_called_once()
        assert cli_config.config == expected_config


def test_list_credentials():
    pass  # TODO


def test_current_credentials():
    pass  # TODO


def test_delete_credentials():
    pass  # TODO


def test_use_credentials():
    pass  # TODO


def test_set_option():
    pass  # TODO


def test_unset_option():
    pass  # TODO


def test_get_option():
    pass  # TODO


def test_list_options():
    pass  # TODO


def test_validate_config():
    pass  # TODO

from aura.config_repository import CLIConfig
from aura.error_handler import CredentialsNotFound
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.credentials import use_credentials


def test_use_credentials(mock_config):
    runner = CliRunner()

    result = runner.invoke(use_credentials, ["test-creds"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == f"Now using credentials test-creds\n"

    mock_config.use_credentials.assert_called_once_with("test-creds")


def test_use_credentials_not_found(mock_config):
    runner = CliRunner()

    mock_config.use_credentials.side_effect = CredentialsNotFound("test-creds")

    result = runner.invoke(use_credentials, ["test-creds"], obj=mock_config)

    assert result.exit_code == 1
    assert result.output == f"Error: Credentials test-creds not found\n"

    mock_config.use_credentials.assert_called_once_with("test-creds")

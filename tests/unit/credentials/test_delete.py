from aura.config_repository import CLIConfig
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.credentials import delete_credentials


def test_delete_credentials(mock_config):
    runner = CliRunner()

    result = runner.invoke(delete_credentials, ["test-creds"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == f"Credentials test-creds successfully deleted\n"

    mock_config.delete_credentials.assert_called_once_with("test-creds")

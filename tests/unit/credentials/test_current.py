from aura.config_repository import CLIConfig
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.credentials import current_credentials


def test_current_credentials():
    runner = CliRunner()

    mock_config = MagicMock(spec=CLIConfig)
    mock_config.current_credentials.return_value = "test", {
        "CLIENT_ID": "test-id",
        "CLIENT_SECRET": "secret",
    }

    result = runner.invoke(current_credentials, [], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == f"Current credentials:\nName:\t\ttest\nClient ID:\ttest-id\n"

    mock_config.current_credentials.assert_called_once()


def test_current_credentials_none_set():
    runner = CliRunner()

    mock_config = MagicMock(spec=CLIConfig)
    mock_config.current_credentials.return_value = None, None

    result = runner.invoke(current_credentials, [], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == f"No credentials have been selected.\n"

    mock_config.current_credentials.assert_called_once()

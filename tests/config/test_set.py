from aura.config_repository import CLIConfig
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.config import set as set_config_option


def test_set_config_option():
    runner = CliRunner()

    mock_config = MagicMock(spec=CLIConfig)

    result = runner.invoke(
        set_config_option, ["default-tenant", "my-tenant-id"], obj=mock_config
    )

    assert result.exit_code == 0
    assert result.output == 'Config option default-tenant set to "my-tenant-id"\n'

    mock_config.set_option.assert_called_once_with("default-tenant", "my-tenant-id")


def test_set_config_option_invalid_option():
    runner = CliRunner()

    mock_config = MagicMock(spec=CLIConfig)
    mock_config.get_option.return_value = None

    result = runner.invoke(set_config_option, ["invalid-value", "no"], obj=mock_config)

    assert result.exit_code == 1
    assert result.output == "Error: No config option invalid-value exists\n"

    mock_config.set_option.assert_not_called()

from aura.config_repository import CLIConfig
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.config import unset as unset_config_option


def test_unset_config_option():
    runner = CliRunner()

    mock_config = MagicMock(spec=CLIConfig)

    result = runner.invoke(unset_config_option, ["default-tenant"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == "Config option default-tenant unset\n"

    mock_config.unset_option.assert_called_once_with("default-tenant")


def test_unset_config_option_invalid_option():
    runner = CliRunner()

    mock_config = MagicMock(spec=CLIConfig)
    mock_config.get_option.return_value = None

    result = runner.invoke(unset_config_option, ["invalid-value"], obj=mock_config)

    assert result.exit_code == 1
    assert result.output == "Error: No config option invalid-value exists\n"

    mock_config.unset_option.assert_not_called()

from aura.config_repository import CLIConfig
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.config import get_option


def test_get_config_option(mock_config):
    runner = CliRunner()

    mock_config.get_option.return_value = "my-tenant-id"

    result = runner.invoke(get_option, ["default_tenant"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == 'Config option default_tenant is set to "my-tenant-id"\n'

    mock_config.get_option.assert_called_once()


def test_get_config_option_not_set(mock_config):
    runner = CliRunner()

    mock_config.get_option.return_value = None

    result = runner.invoke(get_option, ["default_tenant"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == "No value for default_tenant set\n"

    mock_config.get_option.assert_called_once()


def test_get_config_option_invalid_option(mock_config):
    runner = CliRunner()

    mock_config.get_option.return_value = None

    result = runner.invoke(get_option, ["invalid-value"], obj=mock_config)

    assert result.exit_code == 1
    assert result.output == "Error: No config option invalid-value exists\n"

    mock_config.get_option.assert_not_called()

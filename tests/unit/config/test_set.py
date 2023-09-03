from aura.config_repository import CLIConfig
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.config import set_option


def test_set_config_option(mock_config):
    runner = CliRunner()

    result = runner.invoke(set_option, ["default_tenant", "my-tenant-id"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == 'Config option default_tenant set to "my-tenant-id"\n'

    mock_config.set_option.assert_called_once_with("default_tenant", "my-tenant-id")


def test_set_config_option_invalid_option(mock_config):
    runner = CliRunner()

    mock_config.get_option.return_value = None

    result = runner.invoke(set_option, ["invalid-value", "no"], obj=mock_config)

    assert result.exit_code == 1
    assert result.output == "Error: No config option invalid-value exists\n"

    mock_config.set_option.assert_not_called()

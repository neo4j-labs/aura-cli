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


def test_set_output(mock_config):
    runner = CliRunner()

    result = runner.invoke(set_option, ["output", "text"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == 'Config option output set to "text"\n'

    mock_config.set_option.assert_called_once_with("output", "text")


def test_set_auth_url(mock_config):
    runner = CliRunner()

    result = runner.invoke(set_option, ["auth_url", "www.auth.uk"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == 'Config option auth_url set to "www.auth.uk"\n'

    mock_config.set_option.assert_called_once_with("auth_url", "www.auth.uk")


def test_set_base_url(mock_config):
    runner = CliRunner()

    result = runner.invoke(set_option, ["base_url", "www.base.com"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == 'Config option base_url set to "www.base.com"\n'

    mock_config.set_option.assert_called_once_with("base_url", "www.base.com")


def test_set_save_logs(mock_config):
    runner = CliRunner()

    result = runner.invoke(set_option, ["save_logs", "yes"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == 'Config option save_logs set to "yes"\n'

    mock_config.set_option.assert_called_once_with("save_logs", "yes")


def test_set_log_file_path(mock_config):
    runner = CliRunner()

    result = runner.invoke(set_option, ["log_file_path", "path/to/log_file"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == 'Config option log_file_path set to "path/to/log_file"\n'

    mock_config.set_option.assert_called_once_with("log_file_path", "path/to/log_file")

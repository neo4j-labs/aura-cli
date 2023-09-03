from aura.config_repository import CLIConfig
import pytest
from click.testing import CliRunner

from aura.credentials import add_credentials


def test_add_credentials(mock_config):
    runner = CliRunner()

    result = runner.invoke(
        add_credentials,
        [
            "--name",
            "test",
            "--client-id",
            "client-123",
            "--client-secret",
            "super-secret",
        ],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert (
        result.output
        == f'Credentials "test" successfully saved. Now using "test" as credentials.\n'
    )

    mock_config.add_credentials.assert_called_once_with("test", "client-123", "super-secret")

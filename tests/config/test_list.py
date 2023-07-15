from aura.config_repository import CLIConfig
from aura.format import format_text_output
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock

from aura.config import list as list_config_options


def test_list_config_options():
    runner = CliRunner()

    mock_config = MagicMock(spec=CLIConfig)
    mock_config.list_options.return_value = [
        {"Option": "default-tenant", "Value": "my-tenant-id"}
    ]

    result = runner.invoke(list_config_options, [], obj=mock_config)

    assert result.exit_code == 0
    assert (
        result.output
        == format_text_output(
            [{"Option": "default-tenant", "Value": "my-tenant-id"}], printing=False
        )
        + "\n"
    )

    mock_config.list_options.assert_called_once()

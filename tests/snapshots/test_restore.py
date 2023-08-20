from aura.config_repository import CLIConfig
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock, Mock

from aura.snapshots import restore as restore_snapshot


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {}
    return mock_res


def mock_instances_response():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"data": [{"name": "Instance01", "id": "123"}]}
    return mock


def test_restore_snapshot(api_request, mock_config):
    runner = CliRunner()
    mock_config = MagicMock(spec=CLIConfig)
    mock_config.get_option.return_value = None

    api_request.return_value = mock_response()

    result = runner.invoke(
        restore_snapshot,
        ["--instance-id", "123", "--snapshot-id", "789789"],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_once_with(
        "POST",
        "https://api.neo4j.io/v1/instances/123/snapshots/789789/restore",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
    )


def test_restore_snapshot_with_name(api_request, mock_config):
    runner = CliRunner()

    # Mock first call for getting instances and finding the id from the name
    api_request.side_effect = [mock_instances_response(), mock_response()]

    result = runner.invoke(
        restore_snapshot,
        ["--instance-name", "Instance01", "--snapshot-id", "789789"],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_with(
        "POST",
        "https://api.neo4j.io/v1/instances/123/snapshots/789789/restore",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
    )

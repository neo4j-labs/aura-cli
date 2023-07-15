import pytest
from click.testing import CliRunner
from unittest.mock import Mock

from aura.snapshots import list as list_snapshots
from tests.conftest import printed_data


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "data": [
            {
                "instance_id": "123",
                "profile": "Scheduled",
                "snapshots_id": "789789",
                "status": "Completed",
                "timestamp": "2023-06-16T07:38:57Z",
            }
        ]
    }
    return mock_res


def mock_instances_response():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"data": [{"name": "Instance01", "id": "123"}]}
    return mock


def test_list_snapshots(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(list_snapshots, ["--instance-id", "123"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == printed_data(
        [
            {
                "instance_id": "123",
                "profile": "Scheduled",
                "snapshots_id": "789789",
                "status": "Completed",
                "timestamp": "2023-06-16T07:38:57Z",
            }
        ]
    )
    api_request.assert_called_once_with(
        "GET",
        "https://api.neo4j.io/v1beta4/instances/123/snapshots",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        params={},
    )


def test_list_snapshots_with_name(api_request, mock_config):
    runner = CliRunner()

    # Mock first call for getting instances and finding the id from the name
    api_request.side_effect = [mock_instances_response(), mock_response()]

    result = runner.invoke(
        list_snapshots, ["--instance-name", "Instance01"], obj=mock_config
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        [
            {
                "instance_id": "123",
                "profile": "Scheduled",
                "snapshots_id": "789789",
                "status": "Completed",
                "timestamp": "2023-06-16T07:38:57Z",
            }
        ]
    )
    api_request.assert_called_with(
        "GET",
        "https://api.neo4j.io/v1beta4/instances/123/snapshots",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        params={},
    )


def test_list_snapshots_with_date(api_request, mock_config):
    runner = CliRunner()

    # Mock first call for getting instances and finding the id from the name
    api_request.return_value = mock_response()

    result = runner.invoke(
        list_snapshots,
        ["--instance-id", "123", "--date", "2023-01-01"],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        [
            {
                "instance_id": "123",
                "profile": "Scheduled",
                "snapshots_id": "789789",
                "status": "Completed",
                "timestamp": "2023-06-16T07:38:57Z",
            }
        ]
    )

    api_request.assert_called_with(
        "GET",
        "https://api.neo4j.io/v1beta4/instances/123/snapshots",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        params={"date": "2023-01-01"},
    )

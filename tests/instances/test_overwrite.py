import pytest
from click.testing import CliRunner
from unittest.mock import Mock
import json

from aura.instances import overwrite_instance


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


def test_overwrite_instance(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(
        overwrite_instance,
        ["--instance-id", "123", "--source-instance", "456"],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_once_with(
        "POST",
        "https://api.neo4j.io/v1/instances/123/overwrite",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        data=json.dumps({"source_instance_id": "456"}),
        timeout=10,
    )


def test_overwrite_instance_with_name(api_request, mock_config):
    runner = CliRunner()

    # Mock first call for getting instances and finding the id from the name
    api_request.side_effect = [mock_instances_response(), mock_response()]

    result = runner.invoke(
        overwrite_instance,
        ["--name", "Instance01", "--source-instance", "456"],
        obj=mock_config,
    )

    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_with(
        "POST",
        "https://api.neo4j.io/v1/instances/123/overwrite",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        data=json.dumps({"source_instance_id": "456"}),
        timeout=10,
    )

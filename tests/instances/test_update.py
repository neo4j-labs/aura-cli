import pytest
from click.testing import CliRunner
from unittest.mock import Mock
import json

from aura.instances import update as update_instance

def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {}
    return mock_res


def mock_instances_response():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"data": [{"name": "Instance01", "id": "123" }]}
    return mock


def test_update_instance_name(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(update_instance, ["--instance-id", "123", "--new-name", "InstanceTest"], obj=mock_config)
    
    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_once_with(
        "PATCH", 
        "https://api.neo4j.io/v1beta4/instances/123", 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"},
        data=json.dumps({"name": "InstanceTest"})
    )


def test_update_instance_name_with_name(api_request, mock_config):
    runner = CliRunner()

    # Mock first call for getting instances and finding the id from the name
    api_request.side_effect = [mock_instances_response(), mock_response()]

    result = runner.invoke(update_instance, ["--name", "Instance01", "--new-name", "InstanceTest"], obj=mock_config)
    
    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_with(
        "PATCH", 
        "https://api.neo4j.io/v1beta4/instances/123", 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"},
        data=json.dumps({"name": "InstanceTest"})
    )


def test_update_instance_memory(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(update_instance, ["--instance-id", "123", "--memory", "8"], obj=mock_config)
    
    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_once_with(
        "PATCH", 
        "https://api.neo4j.io/v1beta4/instances/123", 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"},
        data=json.dumps({"memory": "8GB"})
    )


def test_update_instance_name_and_memory(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(update_instance, ["--instance-id", "123", "--new-name", "InstanceTest", "--memory", "8"], obj=mock_config)
    
    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_once_with(
        "PATCH", 
        "https://api.neo4j.io/v1beta4/instances/123", 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"},
        data=json.dumps({"memory": "8GB", "name": "InstanceTest"})
    )
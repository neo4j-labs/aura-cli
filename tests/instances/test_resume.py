import pytest
from click.testing import CliRunner
from unittest.mock import Mock
import json

from aura.instances import resume as resume_instance

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


def test_resume_instance(api_request):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(resume_instance, ["--instance-id", "123"])
    
    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_once_with(
        "POST", 
        "https://api.neo4j.io/v1beta3/instances/123/resume", 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"}
    )


def test_resume_instance_with_name(api_request):
    runner = CliRunner()

    # Mock first call for getting instances and finding the id from the name
    api_request.side_effect = [mock_instances_response(), mock_response()]

    result = runner.invoke(resume_instance, ["--name", "Instance01"])
    
    assert result.exit_code == 0
    assert result.output == "Operation successful\n"

    api_request.assert_called_with(
        "POST", 
        "https://api.neo4j.io/v1beta3/instances/123/resume", 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"}
    )
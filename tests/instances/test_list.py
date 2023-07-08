import pytest
from click.testing import CliRunner
from unittest.mock import Mock

from aura.instances import list as list_instances
from tests.conftest import printed_data

def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {"data": [{"id": "123", "name": "Instance01", "tenant_id": "qwe123"}]}
    return mock_res


def test_list_instances(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(list_instances, [], obj=mock_config)
    
    assert result.exit_code == 0
    assert result.output == printed_data([{"id": "123", "name": "Instance01", "tenant_id": "qwe123"}])

    api_request.assert_called_once_with(
        "GET", 
        "https://api.neo4j.io/v1beta4/instances", 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"},
        params={}
    )


def test_list_instances_with_tenant_id(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(list_instances, ["--tenant-id", "qwe123"], obj=mock_config)
    
    assert result.exit_code == 0
    assert result.output == printed_data([{"id": "123", "name": "Instance01", "tenant_id": "qwe123"}])

    api_request.assert_called_once_with(
        "GET", 
        "https://api.neo4j.io/v1beta4/instances", 
        headers={"Content-Type": "application/json", "Authorization": f"Bearer dummy-token"},
        params={ "tenant_id": "qwe123" }
    )
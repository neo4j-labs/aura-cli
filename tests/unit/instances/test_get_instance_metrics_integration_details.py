import pytest
from click.testing import CliRunner
from unittest.mock import Mock

from aura.instances import get_instance_metrics_integration_details
from unit.conftest import printed_data


def mock_response(metrics_endpoint):
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {"data": {"endpoint": metrics_endpoint}}
    return mock_res


def test_get_instance_metrics_integration_details(api_request, mock_config):
    runner = CliRunner()
    metrics_endpoint = "https://customer-metrics-api.neo4j.io/api/456/123/metrics"

    api_request.return_value = mock_response(metrics_endpoint)

    result = runner.invoke(get_instance_metrics_integration_details, ["--instance-id", "123"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == printed_data({"endpoint": metrics_endpoint})

    api_request.assert_called_once_with(
        "GET",
        "https://api.neo4j.io/v1/instances/123/metrics-integration",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        timeout=10,
    )

import pytest
from click.testing import CliRunner
from unittest.mock import Mock

from aura.tenants import get as get_tenant
from tests.conftest import printed_data


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {"data": {"id": "123", "name": "Personal tenant"}}
    return mock_res


def test_get_tenant(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(get_tenant, ["--tenant-id", "123"], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == printed_data({"id": "123", "name": "Personal tenant"})

    api_request.assert_called_once_with(
        "GET",
        "https://api.neo4j.io/v1beta4/tenants/123",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
    )

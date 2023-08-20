import pytest
from click.testing import CliRunner
from unittest.mock import Mock

from aura.tenants import list as list_tenants
from tests.conftest import printed_data


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "data": [{"id": "123", "name": "Personal tenant"}]
    }
    return mock_res


def test_list_tenants(api_request, mock_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(list_tenants, [], obj=mock_config)

    assert result.exit_code == 0
    assert result.output == printed_data(
        [{"id": "123", "name": "Personal tenant"}]
    )

    api_request.assert_called_once_with(
        "GET",
        "https://api.neo4j.io/v1/tenants",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
    )

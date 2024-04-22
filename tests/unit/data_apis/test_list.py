import pytest
from click.testing import CliRunner
from unittest.mock import Mock

from aura.data_apis import list_data_apis
from unit.conftest import printed_data


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "data": [
            {
                "id": "321",
                "name": "GraphQLDataConnector",
                "type": "graphql",
                "status": "ready",
                "aura_instance": {"id": "123"},
                "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
            }
        ]
    }
    return mock_res


def test_list_data_apis(api_request, mock_data_api_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    result = runner.invoke(
        list_data_apis,
        ["--instance-id", "123"],
        obj=mock_data_api_config,
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        [
            {
                "id": "321",
                "name": "GraphQLDataConnector",
                "type": "graphql",
                "status": "ready",
                "aura_instance": {"id": "123"},
                "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
            }
        ]
    )

    api_request.assert_called_once_with(
        "GET",
        "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        timeout=30,
    )

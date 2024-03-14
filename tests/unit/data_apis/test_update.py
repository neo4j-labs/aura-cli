import pytest
import json
import base64
import os

from click.testing import CliRunner
from unittest.mock import Mock

from aura.data_apis import update_data_api
from unit.conftest import printed_data


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "data": {
            "id": "321",
            "name": "GraphQLDataConnector",
            "type": "graphql",
            "status": "updating",
            "aura_instance": {"id": "123"},
            "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
        }
    }
    return mock_res


def test_update_data_api(api_request, mock_data_api_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    name = "data-api"
    instance_username = "neo4j"
    instance_password = "password"

    result = runner.invoke(
        update_data_api,
        [
            "--instance-id",
            "123",
            "--data-api-id",
            "321",
            "--instance-username",
            instance_username,
            "--instance-password",
            instance_password,
            "--name",
            name,
        ],
        obj=mock_data_api_config,
    )

    assert result.exit_code == 0
    assert result.output == printed_data(
        {
            "id": "321",
            "name": "GraphQLDataConnector",
            "type": "graphql",
            "status": "updating",
            "aura_instance": {"id": "123"},
            "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
        }
    )

    api_request.assert_called_once_with(
        "PATCH",
        "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis/321",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        timeout=10,
        data=json.dumps(
            {
                "name": name,
                "aura_instance": {
                    "username": instance_username,
                    "password": instance_password,
                },
            }
        ),
    )


def test_update_data_api_type_definitions(api_request, mock_data_api_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    type_definitions = """type Movie {
        title: String! @unique
    }
    """

    result = runner.invoke(
        update_data_api,
        [
            "--instance-id",
            "123",
            "--data-api-id",
            "321",
            "--type-definitions",
            type_definitions,
        ],
        obj=mock_data_api_config,
    )

    assert result.exit_code == 0
    assert (
        result.output
        == f"""Could not open provided type definitions as file, trying as GraphQL SDL\n{printed_data(
        {
            "id": "321",
            "name": "GraphQLDataConnector",
            "type": "graphql",
            "status": "updating",
            "aura_instance": {"id": "123"},
            "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
        }
    )}"""
    )

    api_request.assert_called_once_with(
        "PATCH",
        "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis/321/graphql",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        timeout=10,
        data=json.dumps(
            {"type_definitions": base64.b64encode(type_definitions.encode()).decode()}
        ),
    )


def test_update_data_api_two_calls(api_request, mock_data_api_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    name = "data-api"
    instance_username = "neo4j"
    instance_password = "password"
    type_definitions = """type Movie {
        title: String! @unique
    }
    """

    result = runner.invoke(
        update_data_api,
        [
            "--instance-id",
            "123",
            "--data-api-id",
            "321",
            "--instance-username",
            instance_username,
            "--instance-password",
            instance_password,
            "--name",
            name,
            "--type-definitions",
            type_definitions,
        ],
        obj=mock_data_api_config,
    )

    assert result.exit_code == 0
    assert (
        result.output
        == f"""Could not open provided type definitions as file, trying as GraphQL SDL\n{printed_data(
        {
            "id": "321",
            "name": "GraphQLDataConnector",
            "type": "graphql",
            "status": "updating",
            "aura_instance": {"id": "123"},
            "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
        }
    )}"""
    )

    assert api_request.call_count == 2

    api_request.assert_any_call(
        "PATCH",
        "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis/321",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        timeout=10,
        data=json.dumps(
            {
                "name": name,
                "aura_instance": {
                    "username": instance_username,
                    "password": instance_password,
                },
            }
        ),
    )

    api_request.assert_any_call(
        "PATCH",
        "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis/321/graphql",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        timeout=10,
        data=json.dumps(
            {"type_definitions": base64.b64encode(type_definitions.encode()).decode()}
        ),
    )


def test_update_data_api_two_calls_with_type_definitions_file(
    api_request, mock_data_api_config
):
    type_definitions_file = "type_definitions.graphql"

    try:
        runner = CliRunner()

        api_request.return_value = mock_response()

        name = "data-api"
        instance_username = "neo4j"
        instance_password = "password"
        type_definitions = """type Movie {
            title: String! @unique
        }
        """

        f = open(type_definitions_file, "w")
        f.write(type_definitions)
        f.close()

        result = runner.invoke(
            update_data_api,
            [
                "--instance-id",
                "123",
                "--data-api-id",
                "321",
                "--instance-username",
                instance_username,
                "--instance-password",
                instance_password,
                "--name",
                name,
                "--type-definitions",
                type_definitions_file,
            ],
            obj=mock_data_api_config,
        )

        assert result.exit_code == 0
        assert result.output == printed_data(
            {
                "id": "321",
                "name": "GraphQLDataConnector",
                "type": "graphql",
                "status": "updating",
                "aura_instance": {"id": "123"},
                "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
            }
        )

        assert api_request.call_count == 2

        api_request.assert_any_call(
            "PATCH",
            "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis/321",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer dummy-token",
            },
            timeout=10,
            data=json.dumps(
                {
                    "name": name,
                    "aura_instance": {
                        "username": instance_username,
                        "password": instance_password,
                    },
                }
            ),
        )

        api_request.assert_any_call(
            "PATCH",
            "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis/321/graphql",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer dummy-token",
            },
            timeout=10,
            data=json.dumps(
                {
                    "type_definitions": base64.b64encode(
                        type_definitions.encode()
                    ).decode()
                }
            ),
        )
    finally:
        if os.path.exists(type_definitions_file):
            os.remove(type_definitions_file)

import pytest
import base64
import json
import os

from click.testing import CliRunner
from unittest.mock import Mock

from aura.data_apis import create_data_api
from unit.conftest import printed_data


def mock_response():
    mock_res = Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        "data": {
            "id": "321",
            "name": "GraphQLDataConnector",
            "type": "graphql",
            "status": "creating",
            "aura_instance": {"id": "123"},
            "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
        }
    }
    return mock_res


def test_create_data_api_with_valid_type_definitions(api_request, mock_data_api_config):
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
        create_data_api,
        [
            "--instance-id",
            "123",
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
            "status": "creating",
            "aura_instance": {"id": "123"},
            "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
        }
    )}"""
    )

    api_request.assert_called_once_with(
        "POST",
        "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        timeout=30,
        data=json.dumps(
            {
                "name": name,
                "type": "graphql",
                "aura_instance": {
                    "username": instance_username,
                    "password": instance_password,
                },
                "data_api": {
                    "graphql": {
                        "type_definitions": base64.b64encode(
                            type_definitions.encode()
                        ).decode()
                    }
                },
            }
        ),
    )


def test_create_data_api_with_invalid_type_definitions(
    api_request, mock_data_api_config
):
    runner = CliRunner()

    api_request.return_value = mock_response()

    name = "data-api"
    instance_username = "neo4j"
    instance_password = "password"
    type_definitions = """notatype Movie {
        title: String! @unique
    }
    """

    result = runner.invoke(
        create_data_api,
        [
            "--instance-id",
            "123",
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

    print(result.output)

    assert result.exit_code == 1
    assert (
        result.output
        == """Could not open provided type definitions as file, trying as GraphQL SDL\nError: Could not parse as GraphQL\nError: An unexpected error occurred\n"""
    )

    api_request.assert_not_called()


def test_create_data_api_with_valid_type_definitions_file(
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
            create_data_api,
            [
                "--instance-id",
                "123",
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
                "status": "creating",
                "aura_instance": {"id": "123"},
                "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
            }
        )

        api_request.assert_called_once_with(
            "POST",
            "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer dummy-token",
            },
            timeout=30,
            data=json.dumps(
                {
                    "name": name,
                    "type": "graphql",
                    "aura_instance": {
                        "username": instance_username,
                        "password": instance_password,
                    },
                    "data_api": {
                        "graphql": {
                            "type_definitions": base64.b64encode(
                                type_definitions.encode()
                            ).decode()
                        }
                    },
                }
            ),
        )
    finally:
        if os.path.exists(type_definitions_file):
            os.remove(type_definitions_file)


def test_create_data_api_with_invalid_type_definitions_file(
    api_request, mock_data_api_config
):
    type_definitions_file = "type_definitions.graphql"

    try:
        runner = CliRunner()

        api_request.return_value = mock_response()

        name = "data-api"
        instance_username = "neo4j"
        instance_password = "password"
        type_definitions = """notatype Movie {
            title: String! @unique
        }
        """

        f = open(type_definitions_file, "w")
        f.write(type_definitions)
        f.close()

        result = runner.invoke(
            create_data_api,
            [
                "--instance-id",
                "123",
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

        print(result.output)

        assert result.exit_code == 1
        assert (
            result.output
            == """Error: Could not parse as GraphQL\nError: An unexpected error occurred\n"""
        )

        api_request.assert_not_called()
    finally:
        if os.path.exists(type_definitions_file):
            os.remove(type_definitions_file)


def test_create_data_api_with_jwks_url(api_request, mock_data_api_config):
    runner = CliRunner()

    api_request.return_value = mock_response()

    name = "data-api"
    instance_username = "neo4j"
    instance_password = "password"
    type_definitions = """type Movie {
        title: String! @unique
    }
    """
    jwks_url = "https://jwks.url/.well-known/jwks.json"

    result = runner.invoke(
        create_data_api,
        [
            "--instance-id",
            "123",
            "--instance-username",
            instance_username,
            "--instance-password",
            instance_password,
            "--name",
            name,
            "--type-definitions",
            type_definitions,
            "--jwks-url",
            jwks_url,
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
            "status": "creating",
            "aura_instance": {"id": "123"},
            "url": "https://321.b03bbb8d00271ccdcf4c289748fe43e2.graphql.neo4j-dev.io/graphql",
        }
    )}"""
    )

    api_request.assert_called_once_with(
        "POST",
        "https://graphql-api-staging.neo4j.io/v1/instances/123/data-apis",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer dummy-token",
        },
        timeout=30,
        data=json.dumps(
            {
                "name": name,
                "type": "graphql",
                "aura_instance": {
                    "username": instance_username,
                    "password": instance_password,
                },
                "data_api": {
                    "graphql": {
                        "type_definitions": base64.b64encode(
                            type_definitions.encode()
                        ).decode()
                    }
                },
                "security": {"jwks": {"url": jwks_url}},
            }
        ),
    )
